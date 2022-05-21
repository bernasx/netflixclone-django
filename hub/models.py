from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    fullname = models.CharField(max_length=200, default='fullname')

class Movie(models.Model):
    title = models.CharField(max_length=200, default='title')
    producer = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField()
    views = models.IntegerField()
    description = models.TextField()
    duration = models.IntegerField()
    lastUpdated = models.DateTimeField()
    isPublic = models.BooleanField()
    isUnlisted = models.BooleanField()
    quality = models.CharField(max_length=200, default='1920x1080')

