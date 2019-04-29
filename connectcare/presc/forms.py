from django import forms
from .models import Presc
from django.forms.fields import DateField
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import DateInput


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Presc
        labels = {'date':'Date','medicine':'Medicine','Notes':'Instructions'}
        fields=['date','medicine','Notes']
        widgets ={
        'date': DateInput(attrs={'type':'date'})
        }
