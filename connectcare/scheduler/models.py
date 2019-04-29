from django.db import models
from profiledet.models import USERMODEL
from django.utils import timezone
from datetime import timedelta
import json
import time


class Appointments(models.Model):
    patient = models.ForeignKey(USERMODEL, related_name='patient_appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(USERMODEL, related_name='doctor_appointments', on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.IntegerField()

    def json_object(self):
        return {
            'date': self.date.isoformat(),
            'end': self.end().isoformat(),
            'patient': self.patient.name,
            'doctor': self.doctor.name,
        }

    def end(self):
        return self.date + timedelta(minutes=self.duration)

    def __repr__(self):
        return '{0} minutes on {1}, {2} with {3}'.format(self.duration, self.date,self.patient, self.doctor)
