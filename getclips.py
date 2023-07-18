from pytube import YouTube
from moviepy.editor import *
from datetime import date
import os

def Download(link, save_path, generic_name):
    name = generic_name + str(len(os.listdir(save_path))) #method of having unique names for everything?

    yt = YouTube(
        link, 
        on_complete_callback=lambda intro, outro, save_path, name: process_vid(intro, outro))
    
    yt = yt.streams.get_highest_resolution(), #get highest resolution
        
        
    try:
       yt.download(output_path=save_path, filename = name)
    except:
        print("Error")

def process_vid(name, path, intro = None, outro = None):
    print("Download finished, starting processing")

    filepath = path + '/' + name
    masterclip = VideoFileClip(filepath)

    if intro is not None:
        pass

    return
        



def main():
    return

if __name__ == "__main__":
    main()