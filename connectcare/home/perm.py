from profiledet.models import USERMODEL
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from connectcare.roles import *
import json
from rolepermissions.checkers import has_role, has_permission, has_object_permission
from rolepermissions.permissions import revoke_permission, grant_permission, available_perm_status, register_object_checker
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from rolepermissions.roles import assign_role, remove_role
from rolepermissions.roles import get_user_roles

def grant_all(role,perm):
	All = User.objects.all()
	for each in All:
		if(has_role(each,role) and not each.is_superuser):
			grant_permission(each,perm)

def revoke_all(role,perm):
	All = User.objects.all()
	for each in All:
		if(has_role(each,role) and not each.is_superuser):
			revoke_permission(each,perm)

def grant(name,perm):
	grant_permission(User.objects.get(username = name),perm)

def revoke(name,perm):
	revoke_permission(User.objects.get(username = name),perm)

def removerole(name,role):

	try:
		q = User.objects.get(username=name)
	except:
		print("No such user exists")
		return

	Users = User.objects.all()
	if(not has_role(q,role) and not q.is_superuser):
		print("No such user of that role exists")
		return
	if(role == "patient"):
		search = "doctor"
	if(role == "doctor"):
		search = "patient"
	for each in Users:
		if(has_role(each,search) and not each.is_superuser):
			p = USERMODEL.objects.get(name=each.username)
			jd = json.decoder.JSONDecoder()
			if(p.auth is not None):
				k = jd.decode(p.auth)
				if(name in k):
					k.remove(name)
					p.auth = json.dumps(k)
					p.save()
	p = USERMODEL.objects.get(name=name)
	p.auth = json.dumps([])
	p.type = "Public"
	p.legit_doctor = 0
	p.save()
	remove_role(q,role)
	assign_role(q,"public")

def authorise_doctor(name):
	try:
		q = USERMODEL.objects.get(name=name,type="Doctor")
	except:
		print("No such doctor exists")
		return
	q.legit_doctor = 1
	q.save()



	# Users = User.objects.all()
	# if(role == "patient"):
	# 	if(not has_role(q,"patient") and not q.is_superuser):
	# 		print("No such patient exists")
	# 	else:
	# 		for each in Users:
	# 			if(has_role(each,"doctor") and not each.is_superuser):
	# 				p = USERMODEL.objects.get(name=each.username)
	# 				jd = json.decoder.JSONDecoder()
	# 				if(p.auth is not None):
	# 					k = jd.decode(p.auth)
	# 					if(name in k):
	# 						k.remove(name)
	# 						p.auth = json.dumps(k)
	# 						p.save()
	# 		p = USERMODEL.objects.get(name=name)
	# 		p.auth = json.dumps([])
	# 		p.type = "Public"
	# 		p.save()
	# 		remove_role(User.objects.get(username=name),"patient")
	# 		assign_role(User.objects.get(username=name),"public")

	# print("asfab")
	# if(role == "doctor"):
	# 	if(not has_role(q,"doctor") and not q.is_superuser):
	# 		print("No such doctor exists")
	# 	else:
	# 		for each in Users:
	# 			if(has_role(each,"patient") and not each.is_superuser):
	# 				p = USERMODEL.objects.get(name=each.username)
	# 				jd = json.decoder.JSONDecoder()
	# 				if(p.auth is not None):
	# 					k = jd.decode(p.auth)
	# 					if(name in k):
	# 						k.remove(name)
	# 						p.auth = json.dumps(k)
	# 						p.save()
	# 		p = USERMODEL.objects.get(name=name)
	# 		p.auth = json.dumps([])
	# 		p.type = "Public"
	# 		p.save()
			# remove_role(User.objects.get(username=name),"doctor")
			# assign_role(User.objects.get(username=name),"public")



