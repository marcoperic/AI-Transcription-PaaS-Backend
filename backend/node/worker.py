import time
import zmq
import urllib.request
import psutil
from threading import Thread
from subsai import SubsAI
from subsai import Tools
import pysubs2

PORT = '9091'
SKIP_LIMIT = 5

class Worker():

    def __init__(self, name) -> None:
        self.ip = urllib.request.urlopen('https://4.ident.me').read().decode('utf8') #get ipv4 address
        self.name = name
        self.work_queue = []
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
        self.transcription_thread = Thread(target=self.transcribe_job)

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
                if (self.cpu_data is not None and self.skips < SKIP_LIMIT):
                    self.connection.send_json({'test': 1}) # take from completed jobs
                    skips += 1
                else:
                    skips = 0
                    self.connection.send_json({self.name: {'average_cpu': self.cpu_data}})
            else:
                if (self.cpu_data is not None): # send CPU data
                    self.connection.send_json({self.name: {'average_cpu': self.cpu_data}})
                else:
                    self.connection.send_json({}) # no data to send

    def process_incoming_data(self):
        pass

    def dispatch(self):
        pass

    def gather_cpu_stats(self):
        # Calling psutil.cpu_precent() for 4 seconds
        print('The CPU usage is: ', psutil.cpu_percent(4))

    '''
    Dequeue from the jobs queue and follow instructions.
    '''
    def solve(self):
        pass

# from subsai import SubsAI
# from subsai import Tools
# import pysubs2

# print('test')
# file = 'test.mp3'
# subs = SubsAI()
# model = subs.create_model('ggerganov/whisper.cpp', {'model_type':'tiny'})
# output = subs.transcribe(file, model)
# output.save('goomba2.srt')

# subtitles = pysubs2.load('goomba2.srt')
# translated_subs = Tools.translate(subtitles, source_language='English', target_language='Croatian', model='facebook/m2m100_1.2B')
# translated_subs.save('translated.srt')

'''
# worker node sample
import time
import zmq

port = 9091

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)
socket.recv()

while True:
    socket.send(b"payload from server: [ip]")
    msg = socket.recv()
    print(msg)
    time.sleep(5)

'''