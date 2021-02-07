from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download', views.download, name='home-download'),
    path('fetchupdate', views.fetch_update, name='home-fetch-update')
]