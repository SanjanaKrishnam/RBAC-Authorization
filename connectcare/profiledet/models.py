from django.db import models
from django.contrib.auth.models import User, UserManager
# Create your models here.
USER_CHOICES = (('Public','PUBLIC'),('Patient','PATIENT'),('Doctor','DOCTOR'),)
BG = (('AB+','AB+'),('AB-','AB-'),('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'))
Gend = (('Male','Male'),('Female','Female'),)
class USERMODEL(models.Model):
    type = models.CharField(max_length = 7, choices = USER_CHOICES,default='public')
    name = models.CharField(max_length = 255,null=True)
    aname = models.CharField(max_length = 255,null=True)
    phno = models.CharField(max_length = 10,null=True)
    dob  = models.DateField(max_length = 8,null=True)
    bg = models.CharField(max_length = 5,choices = BG,default = 'O+',null=True)
    qual = models.CharField(max_length = 255,blank=True,null=True)
    field = models.CharField(max_length = 255,blank= True,null = True)
    sex = models.CharField(max_length = 10,choices = Gend,default = 'M',null=True)
    auth = models.TextField(blank= True,null=True)
    email = models.CharField(max_length=100,null = True)
    legit_doctor = models.IntegerField()



class Extra(models.Model):
    qu = models.CharField(max_length = 255,null = True)
    fi = models.CharField(max_length = 255,null = True)
