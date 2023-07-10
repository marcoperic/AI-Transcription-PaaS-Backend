'''
Utility that keeps track of CPU usage trends for the workers and assigns work to the nodes under the least load. 
'''

from worker_wrapper import Worker

class LoadBalancer():

    TRANSMISSION_DELAY = 1 # number of seconds between data transmissions between worker and wrapper.
    
    def __init__(self, instance) -> None:
        self.master_instance = instance
        self.active_workers = []
    
    '''
    Add a worker to the list of active workers
    '''
    def add_worker(self, name, ip, port, extended):
        print('adding worker, is extended:' + str(extended))
        self.active_workers.append(Worker(self, name, ip, port, [], 0, [], extended))

    '''
    Prints the worker information to console
    '''
    def print_worker_information(self):
        info = []
        for worker in self.active_workers:
            info.append("[{}]: {}, {}, {}".format(worker.ip, worker.name, worker.port, str(worker.extended)))

        return info
            
    '''
    Used to see whether or not any GPU-accelerated workers are online
    '''
    def any_extended_workers(self):
        for worker in self.active_workers:
            if (worker.extended == True):
                return True
        
        return False
    
    '''
    Returns a list of all active workers
    '''
    def get_worker_information(self):
        return self.active_workers

    '''
    Returns a specific worker, found by name or IP. Returns None if worker does not exist.
    '''
    def find_worker(self, name, ip):
        for worker in self.active_workers:
            if (name == worker.name):
                return worker
        
        return None

    '''
    Checks the list of active workers to see which workers are under the most load.
    Workers under the least amount of load are assigned new jobs.
    TODO: sort by cpu load trend and by number of jobs in the queue. 
    '''
    def assign_job(self, job):
        if (len(self.active_workers) == 0):
            raise Exception("Cannot assign job. No active workers.")
        else:
            self.active_workers.sort(key=lambda x: len(x.jobs)) #sorts by number of jobs waiting to be transmitted.
            selection = self.active_workers[0]
            selection.enqueue_job(job)

            # self.active_workers.sort(key=lambda x: x.cpu_trend) # sorts in ascending order, cpu load trend
            # print('workers sorted by cpu_trend:' + str(self.active_workers))
            # selection = self.active_workers[0]
            # selection.enqueue_job(job)

    '''
    Function called by the worker to send a job back to the master.
    '''
    def receive_job(self, job):
        user = str(job['job']['userID'])
        self.master_instance.users_waiting[user] = job

    '''
    Function called by the master to remove a worker. Allows for graceful connection termination?
    TODO: ensure that the worker being deleted has no jobs in the queue.
    '''
    def master_remove_worker(self, name):
        for worker in self.active_workers:
            if worker.name == name:
                worker.terminate_connection()
                worker.destroy()
                return 1
            
        return None

    '''
    To be called by Worker class when exceptions or thrown or connection is closed
    '''
    def remove_worker(self, name):
       for worker in self.active_workers:
           if worker.name == name:
               self.active_workers.remove(worker)