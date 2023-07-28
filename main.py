from getclips import Downloader, VideoProcessor
import os, sys
import argparse
import threading

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--link', help='YouTube video link for download')
    parser.add_argument('--intro', help='Intro length in seconds')
    parser.add_argument('--outro', help= 'Outro length in seconds' )
    args = parser.parse_args()

    save_path = r'videos\spongebob'
    link = 'https://www.youtube.com/watch?v=GfiCTnoqKag'
    
    main_Downloader = Downloader(
        save_path= save_path,
        link= link,
        name= 'spongebob_vid_7252023',
        edit= True
    )

    main_video_path = main_Downloader.video_path()
    main_audio_path = main_Downloader.audio_path()

    print(main_video_path)
    main_vid_processor = VideoProcessor(
        video_path= main_video_path,
        audio_path= main_audio_path,
        intro = 12,
        outro= 411,
        clip_length= 100,
        overlap= 10,
        name= main_Downloader.name
    )

    main_Downloader.callback_object = main_vid_processor

    main_Downloader.download()
    return

if __name__ == "__main__":
    main()