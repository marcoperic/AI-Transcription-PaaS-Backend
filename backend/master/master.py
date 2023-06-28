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
    Add file into dispatch queue. 
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
# m.lb.add_worker('worker-01', 'localhost', 9091)

# http://localhost:3000/testing
@app.route('/testing', methods=['GET'])
def index():
    return "Hello"

# C:\Users\Marco\Documents\GitHub\AI-Transcription-PaaS-Backend\testing>curl -X POST -H "Content-Type: application/json" -d @sample_instructions_package.json http://localhost:3000/upload_media
@app.route('/upload_media', methods=['POST'])
async def upload():
    json = request.get_json()
    json_retval = await m.enqueue(json)
    print('response from async worker nodes ... great!')
    return json_retval

# http://localhost:3000/add_worker?name=worker-01&ip=localhost&port=9091&key=d00d37d8
@app.route('/add_worker', methods=['GET'])
def add_worker():
    name = request.args.get('name')
    ip = request.args.get('ip')
    port = request.args.get('port')
    key = request.args.get('key')
    
    if (key != 'd00d37d8'):
        return 'authentification unsuccessful'
    
    # check that worker with the same name does not already exist
    check = m.lb.get_worker_information('worker-01', 'localhost')

    if (check != None):
        return 'worker already exists'

    m.lb.add_worker(name, ip, int(port))
    return 'successfully added worker!'

@app.route('/get_worker_stats', methods=['GET'])
def get_stats():
    worker_name = request.args.get('name')
    ip = request.args.get('ip')
    key = request.args.get('key')

    if (key != 'd00d37d8'):
            return 'authentification unsuccessful'
    
    print(m.lb.get_worker_information(worker_name, ip).cpu_trend)
    
    return 'success!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)