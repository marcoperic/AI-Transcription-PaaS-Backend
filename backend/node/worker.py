class Worker():

    def __init__(self) -> None:
        pass


'''
# worker node sample
import time
import zmq

port = 9091

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)
socket.recv()

while True:
    socket.send(b"payload from server: [ip]")
    msg = socket.recv()
    print(msg)
    time.sleep(5)

'''