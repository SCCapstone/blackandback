from django.db import models

# Create your models here.
class Photos(models.Model):
    photo = models.ImageField(upload_to="gallery")