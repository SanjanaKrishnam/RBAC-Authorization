from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from profiledet.models import USERMODEL
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import json
from django.http import HttpResponse
from .models import Presc
from .forms import PrescriptionForm
from rolepermissions.checkers import has_permission
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.checkers import has_object_permission
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from django.http import HttpResponseForbidden

@login_required()
@has_permission_decorator('view_pres')
@has_permission_decorator('upload_pres')
def upl(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        return HttpResponseRedirect("/home")
    p = USERMODEL.objects.get(name= request.user.username)
    if request.method =='GET':
        sq = request.GET.get('uploadtest')
        if(has_object_permission('authorised_patient',request.user,User.objects.get(username=sq))):
            if sq == None:
                return HttpResponseRedirect('/home')
            j = USERMODEL.objects.filter(name = sq)
            if not j:
                return HttpResponseRedirect('/home')
            j = USERMODEL.objects.get(name = sq)
            form = PrescriptionForm(request.POST or None)
            context = {'form':form,'names':j.aname,'set':j.name}
            return render(request,'presc/Doctor3rd.html',context)
        else:
            return HttpResponseForbidden()
            
    if request.method == 'POST':
        sq = request.POST.get('uploadtest')
        if(has_object_permission('authorised_patient',request.user,User.objects.get(username=sq))):
            form = PrescriptionForm(request.POST or None)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.doctor = request.user.username
                obj.patient = sq
                obj.save()
                k = '/presc/Patup?Pat_up='
                k = k+str(sq)
                return HttpResponseRedirect(k)
        else:
            return HttpResponseForbidden()


@login_required()
@has_permission_decorator('view_pres')
@has_role_decorator('doctor')
def patup(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        return HttpResponseRedirect("/home")
    p = USERMODEL.objects.get(name= request.user.username)
    if request.method =='GET':
        sq = request.GET.get('Pat_up')
        if sq == None:
            return HttpResponseRedirect('/home')
        j = USERMODEL.objects.filter(name = sq)
        if not j:
            return HttpResponseRedirect('/home')
        if(has_object_permission('authorised_patient',request.user,User.objects.get(username=sq))):
             j = USERMODEL.objects.get(name = sq)
             k = Presc.objects.filter(patient = j.name)
             return render(request,'presc/Doctor2nd.html',{'name':j.aname,'user':j.name,'documents':k})
        else:
            return HttpResponseForbidden()



@login_required()
@has_permission_decorator('view_pres')
def main(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        return HttpResponseRedirect("/home")
    p = USERMODEL.objects.get(name = request.user.username)
    Users = User.objects.all()
    l = []
    if(has_role(request.user,'doctor')):
        for k in Users :
            if(has_object_permission('authorised_patient',request.user,k)):
                z = USERMODEL.objects.get(name = k.username)
                l.append(z)
        return render(request,'presc/Doctorfirst.html',{'name':p.aname,'stuff':l})

    if(has_role(request.user,'patient')):
        k = Presc.objects.filter(patient = p.name)
        return render(request,'presc/Patient.html',{'documents':k})

