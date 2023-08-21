from getclips import Downloader
from  VideoProcessor import VideoProcessor
import os, sys
import argparse
import threading

    


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--link', help='YouTube video link for download')
    parser.add_argument('-n', '--name', help='Enter name for complete video')
    parser.add_argument('-f', '--folder', help='Enter name of folder within \'videos\' directory')
    parser.add_argument('--intro', help='Intro length in seconds')
    parser.add_argument('--outro', help= 'Outro length in seconds' )
    args = parser.parse_args()

    main_video_name = args.name
    folder = args.folder
    link = args.link
    intro = args.intro
    outro = args.outro
    
    save_path = r'videos\\'
    
    save_path = save_path + folder
    
    #if folder doesn't already exist, make it
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    
    
    main_Downloader = Downloader(
        save_path= save_path,
        link= link,
        name= main_video_name,
        edit= True
    )

    main_video_path = main_Downloader.video_path()
    main_audio_path = main_Downloader.audio_path()

    main_vid_processor = VideoProcessor(
        video_path= main_video_path,
        audio_path= main_audio_path,
        intro = intro,
        outro= outro,
        clip_length= 60,
        overlap= 5,
        name= main_Downloader.name
    )

    main_Downloader.callback_object = main_vid_processor
    main_Downloader.download()
    return

if __name__ == "__main__":
    main()