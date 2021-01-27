from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import VideoForm
from .downloader import Downloader


def home(request):
    if request.method == 'POST':
        print(request.POST)
        playlist = 'playlist' in request.POST
        link = request.POST['link']
        downloader = Downloader()
        downloader.fetch(link, playlist)

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
        return render(request, 'home/videos.html', {'forms': forms, 'link': link, 'playlist':playlist})
    return render(request, 'home/home.html')


def download(request):
    if request.method == 'POST':
        print(request.POST)
        link = request.POST['link']
        playlist = True if request.POST['playlist'] == 'True' else False
        titles = request.POST.getlist('title')
        songs = request.POST.getlist('song')
        artists = request.POST.getlist('artist')
        albums = request.POST.getlist('album')

        downloader = Downloader()
        downloader.fetch(link, playlist)

        j = 0
        for i in range(0, len(downloader.videos)):
            if not downloader.videos[i].unavailable:
                downloader.videos[i].title = titles[j]
                downloader.videos[i].song = songs[j]
                downloader.videos[i].artist = artists[j]
                downloader.videos[i].album = albums[j]
                j += 1
        zipfile = downloader.download('home\\static\\home\\music\\')
        return render(request, 'home/downloaded.html', {'videos': downloader.videos, 'file': "home/music/"+zipfile})
