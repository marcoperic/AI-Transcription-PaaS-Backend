import time
import zmq
import urllib.request
import psutil
from threading import Thread
from subsai import SubsAI
from subsai import Tools
import pysubs2
import random

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
        self.work_thread = Thread(target=self.solve)

    def establish_connection(self):
        context = zmq.Context()
        self.connection = context.socket(zmq.PAIR)
        self.connection.bind('tcp://*:%s' % PORT)
        self.connection.recv()

        self.data_transfer_thread = Thread(target=self.data_transfer)
        self.data_transfer_thread.start()

    def data_transfer(self):
        while True:
            incoming = self.connection.recv_json()
            self.process_incoming_data(self, incoming)

            if (len(self.completed_jobs) > 0):
                if (self.cpu_data != None and self.skips < SKIP_LIMIT):
                    self.connection.send_json({'test': 1}) # take from completed jobs
                    skips += 1
                else:
                    skips = 0
                    self.connection.send_json({self.name: {'average_cpu': self.cpu_data}})
            else:
                if (self.cpu_data != None): # send CPU data
                    self.connection.send_json({self.name: {'average_cpu': self.cpu_data}})
                else:
                    self.connection.send_json({}) # no data to send

    def process_incoming_data(self, task):
        if (task['job']['priority'] == 1):
            self.priority_queue.append(task)
        else:
            self.work_queue.append(task)

    def dispatch(self, task):
        pass

    def gather_cpu_stats(self):
        # Calling psutil.cpu_precent() for 4 seconds
        print('The CPU usage is: ', psutil.cpu_percent(4))

    '''
    Dequeue from the jobs queue and follow instructions.
    '''
    def solve(self):
        subs = SubsAI()
        # model = subs.create_model('ggerganov/whisper.cpp', {'model_type':'tiny', 'device':'cpu', 'language': ''})

        while True:
            if (self.priority_queue > 0):
                temp_discriminator = str(random.randint(1,100000))
                temp_file = open(temp_discriminator + '-temp.mp3', 'wb')
                task = self.priority_queue.pop(0)
                file = temp_file.write(task['job']['encoded_media']) # decode from B64 and write to file
                temp_file.close()

                model = subs.create_model('ggerganov/whisper.cpp', {'model_type':'tiny', 'device':'cpu', 'language': task['job']['original_language']})
                transcript = model.transcribe(file, model)
                transcript.save(str(temp_discriminator + '.srt'))

                # now, encode transcript, repackage in task
                

                # did the user want translation? if not, dispatch

            elif (self.work_queue > 0):
                pass
            else:
                time.sleep(1)
                continue