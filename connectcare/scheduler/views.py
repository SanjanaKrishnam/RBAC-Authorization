from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from profiledet.models import USERMODEL
import time
import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils import dateparse
from .models import Appointments
from django.contrib.admin import models
from django.contrib.contenttypes.models import ContentType
from django.utils.text import get_text_list
import json
from django.contrib.auth.models import User
from rolepermissions.checkers import has_permission
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.checkers import has_object_permission
from rolepermissions.decorators import has_role_decorator, has_permission_decorator

@login_required()
@has_permission_decorator('schedule')
def scheduler(request, error=None):
    p = USERMODEL.objects.get(name = request.user.username)
    doctor_list=USERMODEL.objects.filter(type="Doctor")
    patient_list=USERMODEL.objects.filter(type="Patient")
    now = timezone.now()
    if has_role(request.user,'doctor'):
        context = {
        "user": p,
        "doctors": doctor_list,
        "patients": patient_list,
        "schedule_future": Appointments.objects.filter(doctor=p).filter(date__gte=now).order_by('date'),
        "schedule_past": Appointments.objects.filter(doctor=p).filter(date__lt=now).order_by('-date')
    }
    if has_role(request.user,'patient'):
        context = {
            "user": p,
            "doctors": doctor_list,
            "patients": patient_list,
            "schedule_future": Appointments.objects.filter(patient=p).filter(date__gte=now).order_by('date'),
            "schedule_past": Appointments.objects.filter(patient=p).filter(date__lt=now).order_by('-date')
        }
    if error:
        context['error_message'] = error
    return render(request, 'scheduler/schedule.html', context)

def is_free(user, date, duration):
    schedule=Appointments.objects.filter(patient=user) or Appointments.objects.filter(doctor=user)
    end = date + timedelta(minutes=duration)
    for appointment in schedule:
        if (date <= appointment.date <= end or appointment.date <= date <= appointment.end()):
            return False
    return True

def handle_appointment_form(request, body, user, appointment=None):
    date_string = body.get("date")
    try:
        parsed = dateparse.parse_datetime(date_string)
        if not parsed:
            return None, "Invalid date or time."
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
    except:
        return None, "Invalid date or time."
    duration = int(body.get("duration"))
    doctor_id = int(body.get("doctor", user.pk))
    doctor = USERMODEL.objects.get(pk=doctor_id)
    patient_id = int(body.get("patient", user.pk))
    patient = USERMODEL.objects.get(pk=patient_id)

    is_change = appointment is not None

    changed = []
    if is_change:
        if appointment.date != parsed:
            changed.append('date')
        if appointment.patient != patient:
            changed.append('patient')
        if appointment.duration != duration:
            changed.append('duration')
        if appointment.doctor != doctor:
            changed.append('doctor')
        appointment.delete()
    if not is_free(doctor,parsed, duration):
        return None, "The doctor is not free at that time." +\
                     " Please specify a different time."

    if not is_free(patient,parsed, duration):
        return None, "The patient is not free at that time." +\
                     " Please specify a different time."
    appointment = Appointments.objects.create(date=parsed, duration=duration,
                                             doctor=doctor, patient=patient)
  
    if not appointment:
        return None, "We could not create the appointment. Please try again."
    return appointment, None


@login_required()
@has_permission_decorator('schedule')
@has_permission_decorator('add_schedule')
def appointment_form(request, appointment_id):
    p = USERMODEL.objects.get(name=request.user.username)
    if has_role(request.user,'doctor'):
        value="Doctor"
    if has_role(request.user,'patient'):
        value="Patient"
    appointment = None
    doctor_list = USERMODEL.objects.filter(type="Doctor")
    patient_list = USERMODEL.objects.filter(type="Patient")
    if appointment_id:
        appointment = get_object_or_404(Appointments, pk=appointment_id)
    if request.POST:
        appointment, message = handle_appointment_form(
            request, request.POST,
            p, appointment=appointment
        )
        return scheduler(request, error=message)
    context = {
        "user": request.user,
        'appointment': appointment,
        "doctors": doctor_list,
        "patients": patient_list,
        "value":value,

    }
    return render(request, 'scheduler/edit_appointment.html', context)


@login_required()
@has_permission_decorator('schedule')
@has_permission_decorator('add_schedule')
def add_appointment_form(request):
    return appointment_form(request, None)

@login_required()
@has_permission_decorator('schedule')
@has_permission_decorator('delete_schedule')
def delete_appointment(request, appointment_id):
    a = get_object_or_404(Appointments, pk=appointment_id)
    a.delete()
    return redirect('scheduler')
