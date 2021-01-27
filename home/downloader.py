import string
import random
from pytube import YouTube, Playlist
import pathlib
import moviepy.editor as mp
import os
from mutagen.easyid3 import EasyID3
import shutil

class Video:
    def __init__(self, link):
        self.link = link
        try:
            self.video = YouTube(self.link)
            self.unavailable = False
        except BaseException as b:
            print('Video init: ' + b.__str__())
            self.unavailable = True

        self.artist = ''
        self.song = ''
        self.album = ''
        self.title = ''
        self.stream = None
        self.path_video = None
        self.path_audio = None
        self.current_directory = pathlib.Path().absolute().__str__() + '\\'
        self.failed = False

        if not self.unavailable:
            self.assign_info()

    def assign_info(self):
        print(self.video.metadata)
        try:
            self.artist = self.video.metadata[0].get('Artist')
            self.song = self.video.metadata[0].get('Song')
            self.album = self.video.metadata[0].get('Album')
        except IndexError as i:
            #print('Assign info: ' + i.__str__())
            pass

        self.title = self.video.title.replace('|', '')
        self.title = self.title.replace('?', '')

    def download_video(self, path=None):
        self.stream = self.video.streams.filter(only_audio=True).first()
        self.path_video = self.stream.download(
            output_path=self.current_directory + path,
            filename=self.title)

    def convert_to_audio(self, path):
        self.path_audio = self.current_directory + path + self.title + '.mp3'
        new_file = mp.AudioFileClip(self.path_video)
        new_file.write_audiofile(self.path_audio)
        os.remove(self.path_video)

    def add_metadata(self):
        if self.path_audio is not None:
            audio = EasyID3(self.path_audio)
            audio['title'] = self.song
            audio['artist'] = self.artist
            audio['album'] = self.album
            audio.save()

    def download_audio(self, path):
        try:
            self.download_video(path)
            self.convert_to_audio(path)
        except BaseException as b:
            print('Download audio: ' + b.__str__())
            self.failed = True

        try:
            self.add_metadata()
        except ValueError as val:
            #print(val)
            pass


class Downloader:
    def __init__(self):
        self.link = None
        self.is_playlist = None
        self.playlist = None
        self.videos = None
        self.current_directory = pathlib.Path().absolute().__str__() + '\\'

    def fetch(self, link, is_playlist=False):
        self.link = link
        self.is_playlist = is_playlist
        if is_playlist:
            self.playlist = Playlist(self.link)
            self.videos = []
            for v in self.playlist:
                print(v)
                self.videos += [Video(v)]
        else:
            self.videos = [Video(self.link)]

    def download(self, path):
        folder = self.randstring()
        for video in self.videos:
            video.download_audio(path+folder+'\\')
            if video.failed:
                print('failed ' + video.link)
        shutil.make_archive(base_name=self.current_directory+path+folder, format='zip', root_dir=self.current_directory+path, base_dir=folder)
        return folder+'.zip'

    def randstring(self, length=8):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))