from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from profiledet.models import USERMODEL
from .models import Document
from .forms import DocumentForm
from django.http import HttpResponseRedirect
import json
from rolepermissions.checkers import has_permission
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.checkers import has_object_permission
from rolepermissions.decorators import has_role_decorator, has_permission_decorator


@login_required()
@has_permission_decorator('view_records')
def home(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        return HttpResponseRedirect("/home")
    if(has_role(request.user,'patient')):
        documents = Document.objects.filter(user = request.user.username, location = 'Med_HIST')
    if(has_role(request.user,'doctor')):
        Users = User.objects.all()
        documents = Document.objects.none()
        for k in Users :
            if(has_object_permission('authorised_patient',request.user,k)):
                documents = documents|Document.objects.filter(user = k.username, location = 'Med_HIST')  
    return render(request,'uploads/home.html',{'documents':documents})


@login_required()
@has_permission_decorator('view_records')
@has_permission_decorator('upload_records')
def upl(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        return HttpResponseRedirect("/home")
    k = USERMODEL.objects.get(name = request.user.username)
    
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        a = Document()
        a.document.name = filename
        a.user = k.name
        a.description = filename
        a.location = 'Med_HIST'
        a.save()
        return render(request, 'uploads/simple_upload.html', {'uploaded_file_url': uploaded_file_url,'name':filename})
    return render(request, 'uploads/simple_upload.html')

