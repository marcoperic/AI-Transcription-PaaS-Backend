from load_balancer import LoadBalancer
from threading import Thread

'''
Master class that receives data and dispatches 
across multiple worker nodes for processing.
'''
class Master():
    
    def __init__(self) -> None:
        # Instance variables
        self.workers = []
        # Thread declarations
        self.check_for_data = Thread(target = self.check_for_data)
        # Thread initializations
        self.check_for_data.start()

    '''
    Scan file system for new files. When files are added, send to dispatch to coordinate with load balancer.
    '''
    def check_for_data(self):
        pass

    '''
    Read JSON instructions and package file before sending to a node determined by the load balancer
    '''
    def dispatch(self):
        pass

    '''
    Handle incoming data from worker node and send back to the frontend.
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