class Worker():

    def __init__(self) -> None:
        pass

# from subsai import SubsAI
# from subsai import Tools
# import pysubs2

# print('test')
# file = 'test.mp3'
# subs = SubsAI()
# model = subs.create_model('ggerganov/whisper.cpp', {'model_type':'tiny'})
# output = subs.transcribe(file, model)
# output.save('goomba2.srt')

# subtitles = pysubs2.load('goomba2.srt')
# translated_subs = Tools.translate(subtitles, source_language='English', target_language='Croatian', model='facebook/m2m100_1.2B')
# translated_subs.save('translated.srt')

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