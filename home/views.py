import os
import pickle

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import VideoForm
from .downloader import Downloader
from .models import Video


def home(request):
    if request.method == 'POST':
        print(request.POST)
        playlist = 'playlist' in request.POST
        downloader = Downloader()
        try:
            downloader.fetch(request.POST['link'], playlist)
        except BaseException:
            messages.add_message(request, messages.ERROR, 'Invalid link')
            return render(request, 'home/home.html', {'messages': messages.get_messages(request)})

        if not playlist and downloader.videos[0].unavailable:
            messages.add_message(request, messages.ERROR, 'Invalid link')
            return render(request, 'home/home.html', {'messages': messages.get_messages(request)})

        print(downloader)
        identifier = downloader.randstring()
        record = Video(identifier=identifier, downloader=downloader.toBinary(), done=True)
        record.save()
        forms = []
        for video in downloader.videos:
            initial = {'title': video.title,
                       'song': video.song,
                       'artist': video.artist,
                       'album': video.album,
                       }
            metadata = {'unavailable': video.unavailable,
                        'link': video.link
                        }
            forms += [{'form': VideoForm(initial=initial), 'metadata': metadata}]
        return render(request, 'home/videos.html', {'forms': forms,
                                                    'identifier': identifier})
    return render(request, 'home/home.html')


def download(request):
    if request.method == 'POST':
        print(request.POST)
        identifier = request.POST['identifier']
        titles = request.POST.getlist('title')
        songs = request.POST.getlist('song')
        artists = request.POST.getlist('artist')
        albums = request.POST.getlist('album')

        record = Video.objects.get(identifier=identifier).downloader
        downloader = pickle.loads(record)
        print(downloader)

        j = 0
        for i in range(0, len(downloader.videos)):
            if not downloader.videos[i].unavailable:
                downloader.videos[i].title = titles[j]
                downloader.videos[i].song = songs[j]
                downloader.videos[i].artist = artists[j]
                downloader.videos[i].album = albums[j]
                j += 1
        zipfile = downloader.download(os.path.join('static', 'music'))
        return render(request, 'home/downloaded.html', {'videos': downloader.videos, 'file': "music/"+zipfile})
