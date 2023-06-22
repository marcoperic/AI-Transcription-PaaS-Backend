'''
A wrapper class to store statistics and maintain a connection with the remote worker node.
'''

from threading import Thread
import zmq
import time

PORT = '9091'

class Worker():

    def __init__(self, lb, name, ip, jobs, cpu_trend, usage_data) -> None:
        self.lb = lb
        self.name = name
        self.ip = ip
        # self.jobs = jobs # jobs currently being processed by the remote worker.
        self.cpu_trend = cpu_trend
        self.usage_data = usage_data
        self.connection = None

        # establish a connection with the remote worker.
        # TODO: handle the exceptions for when connection fails, etc
        try:
            self.connection_thread = Thread(target=self.establish_connection)
            self.connection_thread.start()
        except:
            print('Exception raised by worker: ' + self.name + ', ip: ' + self.ip)

        self.data_transfer_thread = None
        self.cpu_stats_thread = Thread(target=self.update_cpu_stats)

    def establish_connection(self): # connect to worker node
        context = zmq.Context()
        print('worker ' + self.name + ' attempting connection to ' + self.ip)
        self.connection = context.socket(zmq.PAIR)
        self.connection.connect("tcp://localhost:%s" % PORT)
        print(self.name + ' successfully connected to ' + self.ip)
        self.connection.send_json({'test': 1})

        self.data_transfer_thread = Thread(target=self.data_transfer)
        self.data_transfer_thread.start()

    '''
    The heart of communication between the master and the worker node. Send jobs to the node from the jobs queue.
    Receive responses from the worker and process them using process_worker_response.
    '''
    def data_transfer(self):
        while True:
            msg = self.connection.recv_json() # response from worker
            print(msg)
            # self.process_worker_response(self, msg)

            if (len(self.jobs) > 0):
                self.connection.send_json({'test':1})
            else:
                self.connection.send_json({}) # code to the worker that there are no new jobs.
            time.sleep(self.lb.TRANSMISSION_DELAY)

    '''
    Process the response from the worker. Can be completed jobs or statistics about CPU usage for load balancing.
    : response : JSON package. server code can help ascertain which type of response it is.
    TODO: BE SURE TO REMOVE JOB FROM QUEUE WHEN RESPONSE IS GIVEN
    '''
    def process_worker_response(self, response):
        if ('worker_name' in response):
            self.update_cpu_stats(response)
            return 1
        else:
            self.return_complete_job(response)
            return 0

    '''
    Add a job to the work queue
    '''
    def enqueue_job(self, job):
        self.jobs.append(job)

    '''
    Function to update the CPU usage trend statistic
    '''
    def update_cpu_stats(self, data):
        if (len(self.usage_data) < 100):
            self.usage_data.append(data)
            self.cpu_trend = sum(self.usage_data) / len(self.usage_data)
        else:
            self.usage_data.pop(0)
            self.usage_data.append(data)
            self.cpu_trend = sum(self.usage_data) / 100

    '''
    Send job back to the load balancer and master. Remember to dequeue from list.
    '''
    def return_complete_job(self, job):
        self.lb.receive_job(job)
        #remove the job from the queue
        for x in self.jobs:
            if (x['job']['userID'] == job['job']['userID']):
                self.jobs.remove(x)

    def terminate_connection(self):
        self.connection.close()

    # TODO: verify that this works, check load_balancer too
    def destroy(self):
        self.lb.remove_worker(self.name)