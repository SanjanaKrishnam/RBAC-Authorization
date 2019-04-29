from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.decorators import login_required
from .models import USERMODEL
from .forms import UserTypeForm, ExtraForm
from django.views.generic import TemplateView, ListView, CreateView
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import revoke_permission, grant_permission


@login_required()
def showform(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    if not p:
        form = UserTypeForm(request.POST or None)
        context = {'form':form}
        if form.is_valid():
            obj = form.save(commit=False)
            obj.name = request.user.username
            obj.email = request.user.email
            obj.legit_doctor = 0
            request.user.usertype = obj.type
            obj.save()
            #if(obj.type == 'Doctor'):
                #assign_role(request.user,'doctor')
            if(obj.type == 'Patient'):
                assign_role(request.user,'patient')
            if(obj.type == 'Public'):
                assign_role(request.user,'public')
                return HttpResponseRedirect("/profile")
        return render(request,'profiledet/Profile.html',context)

    else:
        p = USERMODEL.objects.get(name = request.user.username)
        if(p.type == 'Doctor' and p.qual is None):
            form = ExtraForm(request.POST or None)
            context = {'form':form}
            if form.is_valid():
                obj = form.save(commit = False)
                p.qual = obj.qu
                p.field = obj.fi
                p.save()
                return HttpResponseRedirect("/profile")
            return render(request,'profiledet/Profile.html',context)
        else :
            context = {'type':p}
            return render(request,'profiledet/Final.html',context)

                  