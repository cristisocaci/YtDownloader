from django.shortcuts import render


def hello(req, id = 2):
    return render(req, 'home/home.html', {"id": id})
