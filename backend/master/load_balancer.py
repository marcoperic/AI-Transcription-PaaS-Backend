'''
Utility that keeps track of CPU usage trends
for the workers and assigns work to the nodes
under the least load. 
'''

from worker_wrapper import Worker

class LoadBalancer():
    def __init__(self, instance) -> None:
        self.active_workers = []
    
    '''
    Add a worker to the list of active workers
    '''
    def add_worker(self, name, ip):
        print('adding worker')
        self.active_workers.append(Worker(self, name, ip, 0, 0, []))

    '''
    Output the list of workers
    '''
    def print_worker_information(self):
        print(self.active_workers)

    '''
    Checks the list of active workers to see which workers are under the most load.
    Workers under the least amount of load are assigned new jobs.
    '''
    def assign_job(self, job):
        pass

    '''
    Function called by the master to remove a worker. Allows for graceful connection termination?
    TODO: ensure that the worker being deleted has no jobs in the queue.
    '''
    def master_remove_worker(self, name):
        for worker in self.active_workers:
            if worker.name == name:
                worker.terminate_connection()
                worker.destroy()

    '''
    To be called by Worker class when exceptions or thrown or connection is closed
    '''
    def remove_worker(self, name):
       for worker in self.active_workers:
           if worker.name == name:
               self.active_workers.remove(worker)