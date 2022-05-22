from datetime import datetime
from email.policy import default
from fileinput import filename
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class User(AbstractUser):
    fullname = models.CharField(max_length=200, default='fullname')
    avatar = models.ImageField(upload_to='uploads/avatars/', default='uploads/avatars/default.png', blank=True)
    avatar_last_update = models.DateTimeField(default=timezone.now)
    banner = models.ImageField(upload_to='uploads/user_banners/', default='uploads/user_banners/default.png', blank=True)
    banner_last_update = models.DateTimeField(default=timezone.now)

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

    banner = models.ImageField(upload_to='uploads/video_banners/', default='uploads/video_banners/default.png', blank=True)
    banner_last_update = models.DateTimeField(default=timezone.now)

    thumbnail = models.ImageField(upload_to='uploads/video_thumbnails/', default='uploads/video_thumbnails/default.png', blank=True)
    thumbnail_last_update = models.DateTimeField(default=timezone.now)

    storyboard = models.ImageField(upload_to='uploads/video_storyboards/', default='uploads/video_storyboards/default.png', blank=True)
    storyboard_last_update = models.DateTimeField(default=timezone.now)

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
