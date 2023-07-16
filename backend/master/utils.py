import moviepy.editor as mp
import os
import base64
import random

def extract_audio(encoding):
    random_name = str(random.randint(1, 9999999))
    file = open(random_name + '.mp4', 'wb')
    file.write(base64.b64decode(encoding))
    file.close()

    name = str(file).split('.')[0]
    my_clip = mp.VideoFileClip(random_name + '.mp4')
    my_clip.audio.write_audiofile(random_name + '.mp3')
    my_clip.close()
    
    with open(random_name + '.mp4', 'rb') as file:
        encoding = base64.b64encode(file.read())
        

    padding = b'=' * (4 - (len(encoding) % 4))  # Calculate required padding
    encoding += padding

    os.remove(str(random_name + '.mp4'))
    os.remove(str(random_name + '.mp3'))

    return encoding.decode('utf-8')