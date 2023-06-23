import time
import zmq
import urllib.request
import psutil
from threading import Thread
from subsai import SubsAI
from subsai import Tools
import pysubs2
import random
import base64
import json
import os

PORT = '9091'
SKIP_LIMIT = 5

class Worker():

    def __init__(self, name) -> None:
        self.ip = urllib.request.urlopen('https://4.ident.me').read().decode('utf8') #get ipv4 address
        self.name = name
        self.work_queue = []
        self.priority_queue = []
        self.completed_jobs = []
        self.connection = None
        self.cpu_data = None
        self.skips = 0 # number of times to skip the CPU data transmission before sending

        try:
            self.connection_thread = Thread(target=self.establish_connection)
            self.connection_thread.start()
        except:
            print('Exception')

        self.data_transfer_thread = None
        self.cpu_monitoring_thread = Thread(target=self.gather_cpu_stats)
        self.cpu_monitoring_thread.start()
        self.work_thread = Thread(target=self.process_job)
        self.work_thread.start()

    def establish_connection(self):
        print('initializing connection')
        context = zmq.Context()
        self.connection = context.socket(zmq.PAIR)
        self.connection.bind('tcp://*:%s' % PORT)
        self.connection.recv()
        self.connection.send_json({})
        print('connection received! starting data transfer thread')
        self.data_transfer_thread = Thread(target=self.data_transfer)
        self.data_transfer_thread.start()

    def data_transfer(self):
        while True:
            print('data transfer top of loop')
            incoming = self.connection.recv_json()
            # print(incoming['job']['original_language'])
            self.process_incoming_data(incoming)

            if (len(self.completed_jobs) > 0):
                    retval = self.completed_jobs.pop(0)
                    # print(json.dumps(dict(retval)))
                    self.connection.send_json(retval) # take from completed jobs
            else:
                if (self.cpu_data != None): # send CPU data
                    self.connection.send_json({self.name: {'average_cpu': self.cpu_data}})
                    self.cpu_data = None
                else:
                    self.connection.send_json({}) # no data to send

            time.sleep(0.5) # may cause timing problems with other socket? verify no problems here. 

    def process_incoming_data(self, task):

        if (task == {}):
            return

        if (task['job']['priority'] == 1):
            self.priority_queue.append(task)
        else:
            self.work_queue.append(task)

    def dispatch(self, task):
        self.completed_jobs.append(task)

    def gather_cpu_stats(self):
        # Calling psutil.cpu_precent() for 10 seconds
        while True:
            self.cpu_data = psutil.cpu_percent(10)
            # print('The CPU usage is: ', psutil.cpu_percent(10))

    '''
    Dequeue from the jobs queue and follow instructions.
    '''
    def process_job(self):
        subs = SubsAI()
        # model = subs.create_model('ggerganov/whisper.cpp', {'model_type':'tiny', 'device':'cpu', 'language': ''})

        while True:
            if (len(self.priority_queue) > 0):
                task = self.priority_queue.pop(0)
                self.transcribe_and_translate(task, subs)

            elif (len(self.work_queue) > 0):
                task = self.work_queue.pop(0)
                self.transcribe_and_translate(task, subs)
            else:
                time.sleep(1)
                continue
    
    def transcribe_and_translate(self, task, subs):
        temp_discriminator = str(random.randint(1,100000))
        temp_file = open(str(temp_discriminator + '-temp.mp3'), 'wb')
        temp_file.write(base64.b64decode(task['job']['encoded_media'])) # decode from B64 and write to file
        temp_file.close()

        model = subs.create_model('ggerganov/whisper.cpp', {'model_type':'tiny', 'device':'cpu', 'language': task['job']['original_language']})
        transcript = subs.transcribe(str(temp_discriminator + '-temp.mp3'), model)
        transcript.save(str(temp_discriminator + '.srt'))

        # now, encode transcript, repackage in task
        with open(str(temp_discriminator + '.srt'), 'rb') as transcript:
            encoded_transcript = base64.b64encode(transcript.read())
        
        task['job']['encoded_transcript'] = str(encoded_transcript)

        # did the user want translation? if not, dispatch
        if (task['job']['target_language'] != ''):
            subtitles = pysubs2.load(str(temp_discriminator + '.srt'))
            translated_subs = Tools.translate(subtitles, source_language=task['job']['original_language'], target_language=task['job']['target_language'], model='facebook/m2m100_1.2B')
            translated_subs.save('temp-translated.srt')
            with open('temp-translated.srt', 'rb') as translation:
                encoded_translation = base64.b64encode(translation.read())
            
            task['job']['encoded_translation'] = encoded_translation
            self.dispatch(task)
            print('transcription complete!')
            os.remove(str(temp_discriminator + '.srt'))
        else:
            self.dispatch(task)

        os.remove(str(temp_discriminator + '-temp.mp3'))

Worker('worker-01')