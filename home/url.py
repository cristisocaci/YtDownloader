from django.conf.urls import url

from home.views import hello

urlpatterns = [ url(r'^hello/(\d+)/', hello, name='hello')
]