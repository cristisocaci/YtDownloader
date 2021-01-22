from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello(req, id):
    return render(req, 'home.html', {"id":id})
