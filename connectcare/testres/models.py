from django.db import models

# Create your models here.

class Testres(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='')
    doctor = models.CharField(max_length=255,blank=True)
    user = models.CharField(max_length=255,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length = 255,blank = True)
    patient = models.CharField(max_length=255,blank=True)
