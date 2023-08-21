from pytube import YouTube
from moviepy.editor import *
from datetime import date
import os, sys
import argparse
import threading

class VideoProcessor():
    def __init__(self, video_path, audio_path, intro= None, outro= None, clip_length = 90, overlap = 0, name = None, with_audio = True):
        self.video_path = video_path
        self.audio_path = audio_path

        self.intro = intro
        self.outro = outro

        self.clip_length = clip_length
        self.overlap = overlap

        self.video_name = name
        self.with_audio = with_audio
    
    # def create_clips(self): Will be adding this as a method of handling arguments that i want to be able to be managed for example, if im trying to edit a background video with
    #the clips or not

    def create_clips(self):

        #For the case where I want to download videos without audio. Maybe will try to find a better solution to this. Idk I just want a functioning product please
        if self.with_audio == False:
            self.create_clips_no_audio()
            return
        
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
        
        print(self.master_video.duration)
        print(self.end)        
        #Dealing with execess video left over
        if self.master_video.duration - self.end >= 30:
            self.clip_num +=1
            self.start = self.master_video.duration - self.clip_length
            self.end = self.master_video.duration
            self.new_clip = self.master_video.subclip(t_start = self.start, t_end = self.end)
            self.new_audio = self.master_audio.subclip(t_start = self.start, t_end = self.end)

            self.new_audio = CompositeAudioClip([self.new_audio])
            self.new_clip.audio = self.new_audio


            self.new_clip.write_videofile((self.video_path[:(len(self.video_path) - len(self.video_name) -5)] +'\\'+ 'clips\\' + self.video_name + '_clip' + str(self.clip_num) + '.mp4'), audio_codec = 'aac')

        print('done making clips')

    def create_clips_no_audio(self):
        print('Starting Processing')
        self.master_video = VideoFileClip(self.video_path)

        #getting rid of intros or outros
        if self.intro is not None:
            self.master_video = self.master_video.subclip(t_start = self.intro, t_end = self.master_video.duration)

        if self.outro is not None:
            self.master_video = self.master_video.subclip(t_start = 0, t_end = self.outro)

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
            
            print(self.video_path[:(len(self.video_path) - len(self.video_name) -5)])
            self.adjusted_video_path = self.video_path[:(len(self.video_path) - len(self.video_name) -5)]
            self.new_clip.write_videofile(self.adjusted_video_path +'\\'+ 'clips\\' + self.video_name + '_clip' + str(self.clip_num) + '.mp4')
        
       
        #Dealing with execess video left over
        if self.master_video.duration - self.end >= 30:
            self.clip_num +=1
            self.start = self.master_video.duration - self.clip_length
            self.end = self.master_video.duration
            self.new_clip = self.master_video.subclip(t_start = self.start, t_end = self.end)

            self.new_clip.write_videofile(self.video_path[:(len(self.video_path) - len(self.video_name) -5)] +'\\'+ 'clips\\' + self.video_name + '_clip' + str(self.clip_num) + '.mp4')

        print('done making clips')


