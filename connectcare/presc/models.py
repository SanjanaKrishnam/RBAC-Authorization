from django.db import models

# Create your models here.
class Presc(models.Model):
    doctor = models.CharField(max_length=255,null=True)
    patient = models.CharField(max_length=255,null=True)
    date  = models.DateField(max_length = 8,null=True)
    medicine = models.CharField(max_length=255,null=True)
    Notes = models.TextField(null=True)
