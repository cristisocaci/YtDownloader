from django.db import models


class Video(models.Model):
    downloader = models.BinaryField()
    identifier = models.TextField()
    done = models.BooleanField()

