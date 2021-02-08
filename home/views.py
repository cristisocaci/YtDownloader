import os
import pickle
from multiprocessing import Process

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import VideoForm
from .downloader import Downloader
from .models import Video


def home(request):
    if request.method == 'POST':
        print("home: ", request.POST)
        playlist = 'playlist' in request.POST
        downloader = Downloader()
        identifier = downloader.randstring()
        Process(target=downloader.fetch, args=(request.POST['link'], identifier, playlist)).start()

        return render(request, 'home/videos.html', {'identifier': identifier})
    return render(request, 'home/home.html', {'messages': messages.get_messages(request)})


def fetch_update(request):
    try:
        identifier = request.GET.get('identifier', '')
        record = Video.objects.get(identifier=identifier)

        if record.done and record.downloader == b'':
            messages.add_message(request, messages.ERROR, 'Invalid link')
            return HttpResponse("home")

        downloader = pickle.loads(record.downloader)

        if downloader.getTotalLength() > 300 * 60:
            messages.add_message(request, messages.ERROR, 'The videos are too lengthy')
            return HttpResponse("home")

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

        return render(request, 'home/form.html', {'forms': forms, 'done': record.done, 'identifier': identifier})
    except Video.DoesNotExist as ex:
        print("fetch_update:", ex)
        return render(request, 'home/form.html', {'forms': [], 'done': False, 'identifier': identifier})


def download(request):
    if request.method == 'POST':
        print("download: ",request.POST)
        identifier = request.POST['identifier']
        titles = request.POST.getlist('title')
        songs = request.POST.getlist('song')
        artists = request.POST.getlist('artist')
        albums = request.POST.getlist('album')

        record = Video.objects.get(identifier=identifier)
        record.done = False
        record.save()
        downloader = pickle.loads(record.downloader)

        j = 0
        for i in range(0, len(downloader.videos)):
            if not downloader.videos[i].unavailable:
                downloader.videos[i].title = titles[j]
                downloader.videos[i].song = songs[j]
                downloader.videos[i].artist = artists[j]
                downloader.videos[i].album = albums[j]
                j += 1

        Process(target=downloader.download, args=(os.path.join('static', 'music'), identifier)).start()

        return render(request, 'home/downloaded.html', {'identifier': identifier})


def download_update(request):
    identifier = request.GET.get('identifier', '')
    record = Video.objects.get(identifier=identifier)
    downloader = pickle.loads(record.downloader)
    zipfile = identifier + '.zip'
    return render(request, 'home/downupdate.html', {'videos': downloader.videos,
                                                    'done': record.done,
                                                    'file': 'music/' + zipfile})
