from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
from os.path import join

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='/images/')