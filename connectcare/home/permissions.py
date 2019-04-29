from rolepermissions.permissions import register_object_checker
from profiledet.models import USERMODEL
from rolepermissions.checkers import has_role
from django.contrib.auth import get_user_model
import json
from connectcare.roles import Patient
from rolepermissions.permissions import register_object_checker
from connectcare.roles import *

@register_object_checker()
def authorised_doctor(role, p1, p2):
	if (not role == Patient):
		return False
	p = USERMODEL.objects.get(name = p1.username)
	if(p):
		jd = json.decoder.JSONDecoder()
		if(not p.auth):
			return False
		else:
			doctors = jd.decode(p.auth)

	if(has_role(p2,'doctor') and p2.username in doctors):
		return True
	return False

@register_object_checker()
def authorised_patient(role, p1, p2):
	if (not role == Doctor):
		return False
	p = USERMODEL.objects.get(name = p1.username)
	if(p):
		jd = json.decoder.JSONDecoder()
		if(not p.auth):
			return False
		else:
			patients = jd.decode(p.auth)

	if(has_role(p2,'patient') and p2.username in patients):
		return True
	return False