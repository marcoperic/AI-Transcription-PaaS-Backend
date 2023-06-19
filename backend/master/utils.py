import moviepy.editor as mp

class SERVER_CODES:
    CPU_DATA=100
    PAYLOAD=101

def extract_audio(file):
    name = str(file).split('.')[0]
    print(name)
    my_clip = mp.VideoFileClip(file)
    my_clip.audio.write_audiofile(name + '.ogg')
    return str(name + '.ogg')