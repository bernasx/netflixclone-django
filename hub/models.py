from datetime import datetime
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class User(AbstractUser):
    fullname = models.CharField(max_length=200, default='fullname')

class Video(models.Model):
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
    video = models.FileField(upload_to='uploads/videos/', default=None)

class Tag(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200, default='tag')

class View(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

class Follower(models.Model):
    producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='producer')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

class Avatar(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='uploads/avatars/')
     lastUpdated = models.DateTimeField(default=timezone.now)

class Banner(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='uploads/user_banners/')
     lastUpdated = models.DateTimeField(default=timezone.now)

class VideoBanner(models.Model):
     video = models.ForeignKey(Video, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='uploads/video_banners/')
     lastUpdated = models.DateTimeField(default=timezone.now)

class Thumbnail(models.Model):
     video = models.ForeignKey(Video, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='uploads/video_thumbnails/')
     lastUpdated = models.DateTimeField(default=timezone.now)

class Storyboard(models.Model):
     video = models.ForeignKey(Video, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='uploads/video_storyboards/')
     lastUpdated = models.DateTimeField(default=timezone.now)
