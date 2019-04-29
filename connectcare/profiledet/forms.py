from django import forms
from .models import USERMODEL, Extra
from django.forms.fields import DateField
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import DateInput

class UserTypeForm(forms.ModelForm):
    class Meta:
        model = USERMODEL
        labels = {'aname':'Name','type':'Account Type','phno':'Mobile Number','dob':'Date of Birth','bg':'Blood Group','sex':'Sex:'}
        fields = ['aname','type','phno','dob','bg','sex']
        widgets={
        'dob': DateInput(attrs={'type':'date'})
        }

class ExtraForm(forms.ModelForm):
    class Meta:
        model = Extra
        fields =['qu','fi']
        labels = {'qu':'Qualifications','fi':'Field of Expertise'}
