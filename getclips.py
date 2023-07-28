from pytube import YouTube
from moviepy.editor import *
from datetime import date
import os, sys
import argparse
import threading


class Downloader():
    def __init__(self, save_path, link, name, edit=False, callback_object = None):
        self.save_path = save_path
        self.link = link
        self.callback_object = callback_object

        self.yt_object_video = YouTube(self.link, on_complete_callback= self.download_audio)
        self.yt_object_audio = YouTube(self.link, on_complete_callback= self.audio_callback)
        self.edit = edit
        self.name = name

        self.video_name = self.name + '.mp4'
        self.audio_name = self.name + '.webm'

        self.video_stream = self.yt_object_video.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
        self.audio_stream = self.yt_object_audio.streams.filter(only_audio=True).desc().first()

    def download(self):
        
        #doing this separately so I can have the download for the audio be the callback function for the download of the video (sequential downloading)
        

        self.download_video()
        #Using multi-threading to ensure that callback is only executed when both are done
        # self.thread1  = threading.Thread(target=self.download_video)
        # self.thread2 = threading.Thread(target=self.download_audio)

        # #Starting threads to start the processes concurrently
        # self.thread1.start()
        # self.thread2.start()

        # #Waiting for both threads to finish
        # self.thread1.join()
        # self.thread2.join()

        # if self.callback is not None:
        #     self.callback()

        return
        #self.video_stream.download(output_path=self.save_path, filename=self.video_name)
        #self.audio_stream.download(output_path=self.save_path, filename=self.audio_name)

    def download_video(self):
        self.video_stream.download(output_path=self.save_path, filename=self.video_name)

    def download_audio(self, stream=None, save_path= None):
        print('Done with video!')
        self.audio_stream.download(output_path=self.save_path, filename=self.audio_name)

    def audio_callback(self, stream=None, save_path= None):
        if self.callback_object is not None:
            self.callback_object.create_clips()
        else:
            print('No callback object')
        
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


class VideoProcessor():
    def __init__(self, video_path, audio_path, intro= None, outro= None, clip_length = 90, overlap = 0, name = None):
        self.video_path = video_path
        self.audio_path = audio_path

        self.intro = intro
        self.outro = outro

        self.clip_length = clip_length
        self.overlap = overlap

        self.video_name = name
        
    def create_clips(self):
        print('Starting Processing')
        self.master_video = VideoFileClip(self.video_path)
        self.master_audio = AudioFileClip(self.audio_path)

        #getting rid of intros or outros
        if self.intro is not None:
            self.master_video = self.master_video.subclip(t_start = self.intro, t_end = self.master_video.duration)
            self.master_audio = self.master_audio.subclip(t_start = self.intro, t_end = self.master_audio.duration)

        if self.outro is not None:
            self.master_video = self.master_video.subclip(t_start = 0, t_end = self.outro)
            self.master_audio = self.master_audio.subclip(t_start = 0, t_end = self.outro)

        self.start = 0
        self.end = 0

        self.clip_num = 0
        #creating clips (need to edit audio and video separately then merge)
        print("making clips now")
        while (self.end + self.clip_length - self.overlap) <= self.master_video.duration:
            #increment start and end
            self.start = self.start + self.clip_length - self.overlap
            self.end = self.start + self.clip_length

            self.clip_num += 1
            self.new_clip = self.master_video.subclip(t_start = self.start, t_end = self.end)
            self.new_audio = self.master_audio.subclip(t_start = self.start, t_end = self.end)

            self.new_audio = CompositeAudioClip([self.new_audio])
            self.new_clip.audio = self.new_audio

            print(self.video_path[:(len(self.video_path) - len(self.video_name) -5)])
            self.adjusted_video_path = self.video_path[:(len(self.video_path) - len(self.video_name) -5)]
            self.new_clip.write_videofile(self.adjusted_video_path +'\\'+ 'clips\\' + self.video_name + '_clip' + str(self.clip_num) + '.mp4')
        
        #Dealing with execess video left over
        if self.master_video.duration - self.end >= 30:
            self.clip_num +=1
            self.start = self.master_video.duration - self.clip_length
            self.end = self.master_video.duration
            self.new_clip = self.master_video.subclip(t_start = self.start, t_end = self.end)
            self.new_audio = self.master_audio.subclip(t_start = self.start, t_end = self.end)

            self.new_audio = CompositeAudioClip([self.new_audio])
            self.new_clip.audio = self.new_audio


            self.new_clip.write_videofile(self.video_path[:(len(self.video_path) - len(self.video_name) -5)] +'\\'+ 'clips\\' + self.video_name + '_clip' + str(self.clip_num) + '.mp4')

        print('done making clips')
        



        










def main():

    save_path = r'videos\spongebob'
    link = 'https://www.youtube.com/watch?v=GfiCTnoqKag'
    name = 'spongebob_clip_'

    # Download(link, save_path, name, edit=True)

    process_vid( name = 'spongebob_clip_.mp4',
                 vid_path=save_path, audio_path= r'C:\Users\kxfor\OneDrive\Documents\Personal_Projects\TikTok-Content-Generator\videos\spongebob\spongebob_clip_.webm',
                 intro =12, outro=411,
                 manual_start= 90 ,
                 manual_end= 90 +120,
                 clip_name= 'clipx2'
                )

    return

if __name__ == "__main__":
    main()