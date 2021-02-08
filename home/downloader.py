import string
import random
from pytube import YouTube, Playlist
import pathlib
import moviepy.editor as mp
import os
from mutagen.easyid3 import EasyID3
import shutil
import pickle

import django
django.setup()
from .models import Video as VModel


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
        self.current_directory = pathlib.Path().absolute().__str__()
        self.failed = False
        self.done = False

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
            output_path=os.path.join(self.current_directory, path),
            filename=self.title)

    def convert_to_audio(self, path):
        self.path_audio = os.path.join(self.current_directory, path, self.title + '.mp3')
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
        self.current_directory = pathlib.Path().absolute().__str__()

    def fetch(self, link, identifier, is_playlist=False):
        try:
            from django.db import connection
            connection.close()
            self.link = link
            self.is_playlist = is_playlist
            if is_playlist:
                self.playlist = Playlist(self.link)
                self.videos = []
                for v in self.playlist:
                    print(v)
                    self.videos += [Video(v)]
                    try:
                        record = VModel.objects.get(identifier=identifier)
                        record.downloader = self.toBinary()
                    except BaseException as b:
                        print('Fetch',b)
                        record = VModel(identifier=identifier, downloader=self.toBinary(), done=False)
                    record.save()

                record = VModel.objects.get(identifier=identifier)
                record.done = True
                record.save()

            else:
                self.videos = [Video(self.link)]
                record = VModel(identifier=identifier, downloader=self.toBinary(), done=True)
                record.save()

        except BaseException as ex:
            record = VModel(identifier=identifier, done=True)
            record.save()
            print('FetchBaseEx:', ex)

    def download(self, path, folder):
        from django.db import connection
        connection.close()
        for video in self.videos:
            video.download_audio(os.path.join(path,folder))
            if video.failed:
                print('failed ' + video.link)
            video.done = True
            record = VModel.objects.get(identifier=folder)
            record.downloader = self.toBinary()
            record.save()

        shutil.make_archive(base_name=os.path.join(self.current_directory, path, folder), format='zip', root_dir=os.path.join(self.current_directory, path), base_dir=folder)
        shutil.rmtree(os.path.join(self.current_directory, path, folder))

        record = VModel.objects.get(identifier=folder)
        record.done = True
        record.save()


    def randstring(self, length=8):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    def toBinary(self):
        return pickle.dumps(self)

    def getTotalLength(self):
        length = 0
        for video in self.videos:
            if not video.unavailable:
                length += video.video.length
        return length
