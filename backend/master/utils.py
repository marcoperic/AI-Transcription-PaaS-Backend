import moviepy.editor as mp

def extract_audio(file):
    name = str(file).split('.')[0]
    print(name)
    my_clip = mp.VideoFileClip(file)
    my_clip.audio.write_audiofile(name + '.ogg')