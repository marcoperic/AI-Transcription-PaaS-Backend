'''
A wrapper class to store statistics and maintain a connection with the remote worker node.
'''

from threading import Thread
import zmq
import time
import sys

PORT = '9091'

class Worker():


    def __init__(self, lb, name, ip, jobs, cpu_trend, usage_data) -> None:
        self.lb = lb
        self.name = name
        self.ip = ip
        self.jobs = jobs
        self.cpu_trend = cpu_trend
        self.usage_data = usage_data
        self.connection = None

        # establish a connection with the remote worker.
        # TODO: handle the exceptions for when connection fails, etc
        try:
            self.connection_thread = Thread(target=self.establish_connection)
            self.connection_thread.start()
        except:
            print('exception raised by worker: ' + self.name + ', ip: ' + self.ip)

        # set up thread that periodically sends and receives data from worker node
        self.data_transfer_thread = None

    def establish_connection(self): # connect to worker node
        context = zmq.Context()
        print('worker ' + self.name + ' attempting connection to ' + self.ip)
        self.connection = context.socket(zmq.PAIR)
        self.connection.connect("tcp://localhost:%s" % PORT)
        print(self.name + ' successfully connected to ' + self.ip)
        self.connection.send(b'ping!')

        self.data_transfer_thread = Thread(target=self.data_transfer)
        self.data_transfer_thread.start()

    def data_transfer(self):
        while True:
            # msg = self.connection.recv()
            # print(msg)
            self.connection.send(b"client message to server1")
            self.connection.send(b"client message to server2")
            time.sleep(5)

    def send_job(self):
        pass

    def terminate_connection(self):
        self.connection.close()

    # TODO: verify that this works, check load_balancer too
    def destroy(self):
        self.lb.remove_worker(self.name)