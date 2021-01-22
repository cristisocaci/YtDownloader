from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello(req, id):
    text = "<h1>S'appening</h1>"+id
    return HttpResponse(text)

def hello2(req):
    text = "<h1>S'appening 2</h1>"
    return HttpResponse(text)