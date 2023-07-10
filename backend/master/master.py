'''
Master class that receives data and dispatches across multiple worker nodes for processing.
'''
from flask import Flask, request
from load_balancer import LoadBalancer
from threading import Thread
import time

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
            time.sleep(0.5)

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

# http://localhost:3000/testing
@app.route('/testing', methods=['GET'])
def index():
    return "Hello"

# C:\Users\Marco\Documents\GitHub\AI-Transcription-PaaS-Backend\testing>curl -X POST -H "Content-Type: application/json" -d @sample_instructions_package.json http://localhost:3000/upload_media
@app.route('/upload_media', methods=['POST'])
async def upload():
    auth = request.headers.get("Auth")
    if (auth != 'B75XE1gGFJ7g'):
        return {"authentication unsuccessful"}

    json = request.get_json()
    json_retval = await m.enqueue(json)
    return json_retval

# http://localhost:3000/add_worker?name=worker-01&ip=localhost&port=9091&gpu=false&key=d00d37d8
@app.route('/add_worker', methods=['GET'])
def add_worker():
    name = request.args.get('name')
    ip = request.args.get('ip')
    port = request.args.get('port')
    key = request.args.get('key')
    extended = (request.args.get('gpu') == 'true')
    
    if (key != 'd00d37d8'):
        return 'authentification unsuccessful'
    
    # check that worker with the same name does not already exist
    if (m.lb.find_worker(name, ip) != None):
        return 'worker already exists'

    m.lb.add_worker(name, ip, port, extended)
    return 'successfully added worker!'

# http://localhost:3000/remove_worker?name=worker-01&ip=localhost&key=d00d37d8
@app.route('/remove_worker', methods=['GET'])
def remove_worker():
    name = request.args.get('name')
    ip = request.args.get('ip')
    key = request.args.get('key')

    if (key != 'd00d37d8'):
        return 'authentification unsuccessful'
    
    if (m.lb.master_remove_worker(name) == 1):
        return 'worker succcessfully removed'
    elif (m.lb.master_remove_worker(name) == None):
        return 'error: does the worker exist?'

# http://localhost:3000/get_worker_stats?name=worker-01&ip=localhost&key=d00d37d8
@app.route('/gpu_available', methods=['GET'])
def get_stats():
    return str(m.lb.any_extended_workers())

@app.route('/get_worker_info', methods=['GET'])
def get_info():
    key = request.args.get('key')
    if (key != 'd00d37d8'):
        return 'auth failed'

    return str(m.lb.print_worker_information())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)