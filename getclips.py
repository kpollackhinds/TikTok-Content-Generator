from pytube import YouTube
from moviepy.editor import *
from datetime import date
import os, sys
import argparse
import threading
from VideoProcessor import VideoProcessor   


class Downloader():
    def __init__(self, save_path, link, name, edit=False, callback_object = None):
        self.save_path = save_path
        self.link = link
        self.callback_object = callback_object

        self.yt_object_video = YouTube(self.link, 
                                        on_complete_callback= self.download_audio,
                                        )
        self.yt_object_audio = YouTube(self.link, 
                                        on_complete_callback= self.audio_callback,
                                        )
        self.edit = edit
        self.name = name

        self.video_name = self.name + '.mp4'
        self.audio_name = self.name + '.webm'

        self.video_stream = self.yt_object_video.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
        self.audio_stream = self.yt_object_audio.streams.filter(only_audio=True).desc().first()

        if not os.path.isdir(self.save_path + '\\clips'):
            os.mkdir(save_path + '\\clips')


    def download(self):
        
        #doing this separately so I can have the download for the audio be the callback function for the download of the video (sequential downloading)
        self.download_video()
       
        return

    def download_video(self):
        self.video_stream.download(output_path=self.save_path, filename=self.video_name)

    def download_audio(self, stream=None, save_path= None):
        print('Done with video!')
        self.audio_stream.download(output_path=self.save_path, filename=self.audio_name)

    def audio_callback(self, stream=None, save_path= None):
        if self.callback_object is not None and self.edit:
            self.callback_object.create_clips()
        else:
            print('No editing done')
        
        return
        
    @property
    def video_streams_list(self, first = False):
        if first:
            return self.yt_object_video.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
        
        return self.yt_object_video.streams.filter(file_extension='mp4').order_by('resolution').desc()
    
    def audio_streams_list(self, first = False):
        if first:
            return self.yt_object_audio.streams.filter(only_audio=True).desc().first()
        
        return self.yt_object_audio.streams.filter(only_audio=True).desc()
    
    def video_path(self):
        path = self.save_path + "\\" + self.video_name
        return path
    
    def audio_path(self):
        path = self.save_path + "\\" + self.audio_name
        return path



def main():

    background_video_downloader = Downloader(
        save_path= r'videos\\background_vids',
        link= 'https://www.youtube.com/watch?v=RAVocWnVeoc&ab_channel=SatisfyingVideos',
        name= 'oddle_satisy_comp_1',
        edit= False,
    )

    background_video_downloader.download()
    # save_path = r'videos\spongebob'
    # link = 'https://www.youtube.com/watch?v=GfiCTnoqKag'
    # name = 'spongebob_clip_'

    # # Download(link, save_path, name, edit=True)

    # process_vid( name = 'spongebob_clip_.mp4',
    #              vid_path=save_path, audio_path= r'C:\Users\kxfor\OneDrive\Documents\Personal_Projects\TikTok-Content-Generator\videos\spongebob\spongebob_clip_.webm',
    #              intro =12, outro=411,
    #              manual_start= 90 ,
    #              manual_end= 90 +120,
    #              clip_name= 'clipx2'
    #             )

    return

if __name__ == "__main__":
    main()