# import json

# fp = open('docs/sample_instructions.json')
# x = json.load(fp)
# x['job']['userID'] = '1231iu23u1231nksajnasd98asnd9'
# print(x)

from subsai import SubsAI
from subsai import Tools
import pysubs2
from datetime import datetime

print(datetime.now())
file = 'test.mp3'
subs = SubsAI()
model = subs.create_model('openai/whisper', {'model_type':'base', 'device':'cpu', 'language': 'nl'})
output = subs.transcribe(file, model)
output.save('multiple_language_transcription.srt')
print(datetime.now())


# subtitles = pysubs2.load('goomba2.srt')
# translated_subs = Tools.translate(subtitles, source_language='English', target_language='Croatian', model='facebook/m2m100_1.2B')
# translated_subs.save('translated.srt')