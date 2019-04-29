from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='')
    user = models.CharField(max_length=255,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length = 255,blank = True)
