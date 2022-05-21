from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    fullname = models.CharField(max_length=200, default='fullname')
    isProducer = models.BooleanField(default=False)
