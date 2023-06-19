'''
A wrapper class to store statistics and maintain a connection with the remote worker node.
'''

from threading import Thread

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
            self.connection_thread = Thread(target = self.establish_connection)
        except:
            print('exception raised by worker: ' + self.name + ', ip: ' + self.ip)

    def establish_connection(self): # connect to worker node
        pass

    def send_job(self):
        pass

    def terminate_connection(self):
        pass

    # TODO: verify that this works, check load_balancer too
    def destroy(self):
        self.lb.remove_worker(self.name)
