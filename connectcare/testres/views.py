from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from profiledet.models import USERMODEL
from .models import Testres
from django.http import HttpResponseRedirect
import json
from django.contrib.auth.models import User
from rolepermissions.checkers import has_permission
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.checkers import has_object_permission
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from django.http import HttpResponseForbidden


@login_required()
@has_permission_decorator('view_results')
@has_permission_decorator('upload_results')
def docfin(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        return HttpResponseRedirect("/home")
    p = USERMODEL.objects.get(name= request.user.username)
    if request.method =='GET':
        sq = request.GET.get('uploadtest')
        if sq == None:
            return HttpResponseRedirect('/home')
        j = USERMODEL.objects.filter(name = sq)
        if not j:
            return HttpResponseRedirect('/home')
        j = USERMODEL.objects.get(name = sq)
        return render(request,'testres/DoctorUploadMain.html',{'names':j.aname})
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        k = request.POST.get('patientname')
        l = USERMODEL.objects.get(aname = k)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        a = Testres()
        a.document.name = filename
        a.user = p.name
        a.patient = l.name
        a.doctor = p.aname
        a.description = filename
        a.location = 'TestRes'
        a.save()
        return render(request, 'testres/DoctorUploadMain.html', {'names':k,
        'uploaded_file_url': uploaded_file_url,'name':filename
        })


@login_required()
@has_permission_decorator('view_results')
@has_role_decorator('doctor')
def testup(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        return HttpResponseRedirect("/home")
    p = USERMODEL.objects.get(name= request.user.username)
    if request.method =='GET':
        sq = request.GET.get('Pat_test_up')
        if sq == None:
            return HttpResponseRedirect('/home')
        j = USERMODEL.objects.filter(name = sq)
        if not j:
            return HttpResponseRedirect('/home')
        if(has_object_permission('authorised_patient',request.user,User.objects.get(username=sq))):
            j = USERMODEL.objects.get(name = sq)
            k = Testres.objects.filter(user = p.name, patient = j.name)
            return render(request,'testres/DoctorUploadHome.html',{'name':j.aname,'user':j.name,'documents':k})
        else:
             return HttpResponseForbidden()


@login_required
@has_permission_decorator('view_results')
def main(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        return HttpResponseRedirect("/home")
    p = USERMODEL.objects.get(name= request.user.username)
    Users = User.objects.all()
    l = []
    if(has_role(request.user,'doctor')):
        for k in Users :
            if(has_object_permission('authorised_patient',request.user,k)):
                z = USERMODEL.objects.get(name = k.username)
                l.append(z)
        return render(request,'testres/doc.html',{'name':p.aname,'stuff':l})

    if(has_role(request.user,'patient')):
        k = Testres.objects.filter(patient = p.name)
        return render(request,"testres/pat.html",{'documents':k})


