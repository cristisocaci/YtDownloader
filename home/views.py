from django.shortcuts import render, redirect
from django.http import HttpResponse
import time
from .downloader import Downloader

downloader = Downloader()


def home(request):
    if request.method == 'POST':
        print(request.POST)
        playlist = 'playlist' in request.POST
        downloader.fetch(request.POST['link'], playlist)
        return redirect('home-videos',)
    return render(request, 'home/home.html')


def videos(request):
    context = {'videos': downloader.videos}
    return render(request, 'home/videos.html', context)
