'''
Master class that receives data and dispatches across multiple worker nodes for processing.
'''
from flask import Flask, request
from load_balancer import LoadBalancer
from threading import Thread
import time

MEDIA_DIR = 'backend/master/media/'
app = Flask(__name__)

class Master():
    
    def __init__(self) -> None:
        # Instance variables
        self.workers = []
        self.file_queue = []
        self.users_waiting = dict()
        self.lb = LoadBalancer(self)

        # Thread declarations
        self.dispatch_thread = Thread(target = self.dispatch)

        # Thread initializations
        self.dispatch_thread.start()

    '''
    Add file and its instructions into the dispatch queue. Instruction file and media file are of the same name.
    Keys in the JSON file include: file size, extension, original language, target language
    '''
    async def enqueue(self, instructions):
        userID = instructions['job']['userID']
        self.file_queue.append(instructions)
        self.users_waiting[userID] = ''
        while self.users_waiting[userID] == '':
            print('waiting')
            time.sleep(1)

        retval = self.users_waiting[userID]
        del self.users_waiting[userID]
        return retval

    '''
    Read JSON instructions and package file before sending to a node determined by the load balancer
    Grab the audio track from the file and send it to be transcribed by a worker
    '''
    def dispatch(self):
        while True:
            if (len(self.file_queue) > 0):
                instructions = self.file_queue.pop(0)
                self.lb.assign_job(instructions)

    '''
    Add a worker to the worker list.
    '''
    def add_worker(self, name, ip):
        self.lb.add_worker(name, ip)

    '''
    Remove a worker from the worker list.
    '''
    def remove_worker(self, name):
        self.lb.master_remove_worker(name)

m = Master()
m.lb.add_worker('worker-01', 'localhost', 9091)

# http://localhost:3000/testing
@app.route('/testing', methods=['GET'])
def index():
    return "Hello"


# C:\Users\Marco\Documents\GitHub\AI-Transcription-PaaS-Backend\testing>curl -X POST -H "Content-Type: application/json" -d @sample_instructions_package.json http://localhost:3000/upload_media

@app.route('/upload_media', methods=['POST'])
async def upload():
    # print(request.get_json())
    json = request.get_json()
    json_retval = await m.enqueue(json)
    print('response from async worker nodes ... great!')
    return json_retval

if __name__ == "__main__":
    # m.lb.add_worker('worker-01', 'localhost', 9091) # default port is 9091
    # fp = open('testing/sample_instructions_package.json')
    # x = json.load(fp)
    # m.enqueue(x)
    app.run(host='0.0.0.0', port=3000)