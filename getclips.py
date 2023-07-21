from pytube import YouTube
from moviepy.editor import *
from moviepy.video.io.html_tools import ipython_display
from datetime import date
import os

def Download(link, save_path, generic_name, edit = False):
    # name = generic_name + str(len(os.listdir(save_path))) + '.mp4' #method of having unique names for everything?
    name = generic_name + '.mp4' #method of having unique names for everything?

    x =1 
    y = 2
    yt = YouTube(
        link, 
        on_complete_callback=lambda stream = None, path = None, intro=None, outro=None, save_path=save_path, name=name: process_vid(name, save_path, intro = intro, outro=outro)
        )
    
    mp4files = yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first() 

    print(mp4files)

     
    print(os.listdir(save_path))

    if name not in os.listdir(save_path):
        mp4files.download(output_path=save_path, filename = name)
    else:
        print('File already exists')
        if edit:
            process_vid(name, save_path)
        return
    
    
    # try:
    #     if name not in os.listdir(save_path):
    #         mp4files.download(output_path=save_path, filename = name)
    #     else:
    #         print('File already exists')
    #         return
    # except:
    #     print("Error")
        

def test(x = None, y=None):
    print(x)
    print(y)
    return

def process_vid(name, path, intro = None, outro = None):
    print("Download finished, starting processing")

    filepath = path + '\\' + name
    masterclip = VideoFileClip(filepath)
    
    if intro is not None:
        masterclip = masterclip.subclip(t_start = intro, t_end = masterclip.duration)
    if outro is not None:
        masterclip = masterclip.subclip(t_start = 0, t_end= outro)

    clip_duration = 90 #90 second duration
    overlap = 10 #10 second overlap
    start = 0
    end = clip_duration
    approval = ''
    done = False
    clip_num = 1
    while not done:
        new_clip = masterclip.subclip(t_start = start, t_end = end)
        new_clip.write_videofile(path + '\\'+ 'clips\\'+'CLIP' + str(clip_num)+'.mp4')
        done = True if input("Done viewing? ") == 'y' else False
        clip_num +=1 
        break
        


    return
        



def main():
    save_path = r'videos\spongebob'
    link = 'https://www.youtube.com/watch?v=GfiCTnoqKag'
    name = 'spongebob_clip_'

    Download(link, save_path, name, edit=True)

    return

if __name__ == "__main__":
    main()