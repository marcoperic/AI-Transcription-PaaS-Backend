'''
Worker node class. Accepts incoming connections from master's worker wrapper and completes tasks.
'''

import time
import zmq
import urllib.request
import psutil
import time
from threading import Thread
from subsai import SubsAI
from subsai import Tools
import pysubs2
import random
import base64
import sys
import os

subs = SubsAI()
#warmup 
# subs.create_model('m-bain/whisperX', {'model_type':'medium.en', 'device':'cpu'})
# supported_languages = ['en', 'fr', 'de', 'es', 'it', 'ja', 'zh', 'nl', 'uk', 'pt']
supported_languages = ['en', 'fr', 'es', 'uk']


models = {}
for lang in supported_languages:
    print('Initializing ' + lang + ' model')
    if (lang == 'en'):
        models[lang] = subs.create_model('m-bain/whisperX', {'model_type':'medium', 'device':'cuda', 'language': lang})

    models[lang] = subs.create_model('m-bain/whisperX', {'model_type':'small', 'device':'cuda', 'language': lang, 'batch_size': 2})

class Worker():

    def __init__(self, name) -> None:
        if (len(sys.argv) == 1):
            print('no port provided: defaulting to port 9091')
            self.port = '9091'
        else:
            self.port = str(sys.argv[1])
            print('using port: ' + self.port)

        self.ip = urllib.request.urlopen('https://4.ident.me').read().decode('utf8') #get ipv4 address
        self.name = name
        self.work_queue = []
        self.priority_queue = []
        self.completed_jobs = []
        self.connection = None
        self.cpu_data = None
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

    '''
    Allow incoming connection from master's worker_wrapper
    '''
    def establish_connection(self):
        print('initializing connection')
        context = zmq.Context()
        self.connection = context.socket(zmq.PAIR)
        self.connection.bind('tcp://0.0.0.0:%s' % self.port)
        self.connection.recv()
        self.connection.send_json({})
        self.data_transfer_thread = Thread(target=self.data_transfer)
        self.data_transfer_thread.start()

    '''
    Transfer data to master's worker_wrapper
    '''
    def data_transfer(self):
        while True:
            # print('data transfer top of loop')
            incoming = self.connection.recv_json()
            # print(incoming['job']['original_language'])
            self.process_incoming_data(incoming)

            if (len(self.completed_jobs) > 0):
                    self.connection.send_json(self.completed_jobs.pop(0)) # take from completed jobs
            else:
                if (self.cpu_data != None): # send CPU data
                    self.connection.send_json({'cpu_data': {'worker_name': self.ip, 'average_cpu': self.cpu_data}})
                    self.cpu_data = None
                else:
                    self.connection.send_json({}) # no data to send

            time.sleep(0.5) # may cause timing problems with other socket? verify no problems here. 

    '''
    Processes data sent from the worker wrapper. Accomodates priority queue.
    '''
    def process_incoming_data(self, task):

        if (task == {}):
            return

        if (task['job']['priority'] == 1):
            self.priority_queue.append(task)
        else:
            self.work_queue.append(task)

    '''
    Put the completed transcription/translation job in the 
    '''
    def dispatch(self, task):
        self.completed_jobs.append(task)

    '''
    Collect statistics about CPU utilization and send it to the worker_wrapper
    '''
    def gather_cpu_stats(self):
        # Calling psutil.cpu_precent() for 10 seconds
        while True:
            self.cpu_data = psutil.cpu_percent(3)
            # print('The CPU usage is: ', psutil.cpu_percent(10))

    '''
    Dequeue from the jobs queue and follow instructions.
    '''
    def process_job(self):
        while True:
            if (len(self.priority_queue) > 0):
                task = self.priority_queue.pop(0)
                self.transcribe_and_translate(task)

            elif (len(self.work_queue) > 0):
                task = self.work_queue.pop(0)
                self.transcribe_and_translate(task)
            else:
                time.sleep(1)
                continue
    
    '''
    Handles the transcription and translation workflow and sends it to dispatch()
    '''
    def transcribe_and_translate(self, task):
        language = task['job']['original_language']
        model = models[language]

        now = time.time() * 1000
        temp_discriminator = str(random.randint(1,100000))
        temp_file = open(str(temp_discriminator + '-temp.mp3'), 'wb')
        temp_file.write(base64.b64decode(task['job']['encoded_media'])) # decode from B64 and write to file
        temp_file.close()

        transcript = subs.transcribe(str(temp_discriminator + '-temp.mp3'), model)
        transcript.save(str(temp_discriminator + '.srt'))

        # now, encode transcript, repackage in task
        with open(str(temp_discriminator + '.srt'), 'rb') as transcript:
            encoded_transcript = base64.b64encode(transcript.read())
        
        task['job']['encoded_transcript'] = str(encoded_transcript.decode())

        # did the user want translation? if not, dispatch
        if (task['job']['target_language'] != ""):
            subtitles = pysubs2.load(str(temp_discriminator + '.srt'))
            translated_subs = Tools.translate(subtitles, source_language="", target_language=task['job']['target_language'], model='facebook/m2m100_1.2B') # must have source language
            translated_subs.save('temp-translated.srt')
            with open('temp-translated.srt', 'rb') as translation:
                encoded_translation = base64.b64encode(translation.read())
            
            task['job']['encoded_translation'] = encoded_translation.decode('utf-8')
            self.dispatch(task)
            print('transcription complete!')
            os.remove(str(temp_discriminator + '.srt'))
        else:
            self.dispatch(task)

        os.remove(str(temp_discriminator + '-temp.mp3'))
        os.remove(str(temp_discriminator + '.srt'))
        print('all done! elapsed time: ' + str((time.time()*1000) - now) + 'ms')

Worker('worker-xx')