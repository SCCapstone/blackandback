from django.db import models

# Create your models here.
from django.db import models

username = "crdavis"

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=username + "/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

