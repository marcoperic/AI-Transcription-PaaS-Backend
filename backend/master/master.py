from load_balancer import LoadBalancer
from threading import Thread
from pathlib import Path
from time import sleep
import ffmpeg
import json
import os

MEDIA_DIR = 'backend/master/media/'

'''
Master class that receives data and dispatches 
across multiple worker nodes for processing.
'''
class Master():
    
    def __init__(self) -> None:
        # Instance variables
        self.workers = []
        self.file_queue = []

        # Thread declarations
        # self.check_for_data_thread = Thread(target = self.check_for_data)
        self.dispatch_thread = Thread(target = self.dispatch)

        # Thread initializations
        # self.check_for_data.start()
        self.dispatch_thread.start()

    '''
    Add file and its instructions into the dispatch queue. Instruction file and media file are of the same name.
    Keys in the JSON file include: file size, extension, original language, target language
    '''
    def enqueue(self, fileName, ext):
        file = MEDIA_DIR + fileName + '.' + ext
        instructions = MEDIA_DIR + '.json'
        # instructions = json.load(instructions)
        self.file_queue.append((file, instructions))
        print('successfully enqueued ' + fileName)

    '''
    Read JSON instructions and package file before sending to a node determined by the load balancer
    '''
    def dispatch(self):
        while True:
            if (len(self.file_queue) > 0):
                file, instructions = self.file_queue.pop(0)
                file = r"{}".format(file)
                extension = str('' + file).split('.')[1]
                # print(file)
                print(ffmpeg.probe(file))                
    '''
    Handle incoming data from worker node and send back to the frontend. Delete the files in directory.
    '''
    def receive_worker_data(self):
        pass

    '''
    Add a worker to the worker list.
    '''
    def add_worker(self, name, ip):
        pass

    '''
    Remove a worker from the worker list.
    '''
    def remove_worker(self, name):
        pass
    
    def test(self):
        print('lb test')

if __name__ == "__main__":
    m = Master()
    lb = LoadBalancer(m)
    m.enqueue('kitten', 'jfif')