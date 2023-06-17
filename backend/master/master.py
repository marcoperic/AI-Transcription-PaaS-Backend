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
        self.receive_data_thread = Thread(target = self.receive_data)
        # Thread initializations
        self.receive_data_thread.start()

    '''
    Scan file directory for new files. When files are added, handle appropriately.
    '''
    def receive_data(self):
        pass

if __name__ == "__main__":
    Master()