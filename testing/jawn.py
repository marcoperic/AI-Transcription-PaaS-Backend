import json
import base64
from subsai import SubsAI
from subsai import Tools
import pysubs2
from datetime import datetime
from pywhispercpp.model import Model

# fp = open('docs/sample_instructions.json')
# x = json.load(fp)
# x['job']['userID'] = '1231iu23u1231nksajnasd98asnd9'
# print(x)


# print(datetime.now())
# file = 'test.mp3'
# subs = SubsAI()
# print(subs.available_models())
# model = subs.create_model('guillaumekln/faster-whisper', {'model_type':'base', 'device':'cpu'})
# output = subs.transcribe(file, model)
# output.save('multiple_language_transcription.srt')
# print(datetime.now())


# subtitles = pysubs2.load('goomba2.srt')
# translated_subs = Tools.translate(subtitles, source_language='English', target_language='Croatian', model='facebook/m2m100_1.2B')
# translated_subs.save('translated.srt')


with open('medium_test.mp3', 'rb') as file:
    encoding = base64.b64encode(file.read())

output = open('out.txt', 'wb')
output.write(encoding)
output.close()

# output = open('xyz.srt', 'wb')
# decoded = base64.b64decode('MQ0KMDA6MDA6MDAsMDAwIC0tPiAwMDowMDoxNywxODANCk1hbCBpcyBzb21lYm9keSDrjZTruJQgcG9ydGENCg0K')
# output.write(decoded)
# output.close()