from django.conf.urls import url

from home.views import hello, hello2

urlpatterns = [ url(r'^hello/(\d+)/', hello, name='hello'),
                url('hello2/', hello2, name='hello2')
]