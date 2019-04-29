from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiledet.models import USERMODEL
import json
from django_private_chat.models import Dialog
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rolepermissions.checkers import has_permission
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.checkers import has_object_permission
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from django.http import HttpResponseForbidden
from rolepermissions.roles import assign_role, remove_role
from rolepermissions.roles import get_user_roles



@login_required()
#@has_role_decorator('doctor')
@has_permission_decorator('view_patients')
def pat(request):
    p = USERMODEL.objects.get(name = request.user.username)
    Users = User.objects.all()
    l = []
    for k in Users :
        if(has_object_permission('authorised_patient',request.user,k)):
            z = USERMODEL.objects.get(name = k.username)
            l.append(z)
    return render(request,'home/patres.html',{'name':p.aname,'stuff':l})

@login_required()
#@has_role_decorator('patient')
@has_permission_decorator('authorize')
def auth(request):
    p = USERMODEL.objects.get(name = request.user.username)
    if request.method == 'GET':
        sq = request.GET.get('docauth')
        sq = USERMODEL.objects.get(name = sq)
        if p.auth is None :
            p.auth = json.dumps([])
            p.save()
        if sq.auth is None:
            sq.auth = json.dumps([])
            sq.save()
        jd = json.decoder.JSONDecoder()
        k = jd.decode(sq.auth)
        if p.name not in k:
            k.append(p.name)
            sq.auth = json.dumps(k)
            sq.save()
            k = jd.decode(p.auth)
            k.append(sq.name)
            p.auth = json.dumps(k)
            p.save()
        #user = get_object_or_404(get_user_model(), username=sq.name)
        #Dialog.objects.create(owner = request.user, opponent = user)
        return render(request,'home/docprof.html',{'type':sq,'auth' : 1})

#@has_role_decorator(['patient','doctor'])
@has_permission_decorator('search')
@login_required()
def doc(request):
    #p = USERMODEL.objects.get(name = request.user.username)
    if request.method == 'GET':
        sq = request.GET.get('docpr')
        if sq == None:
            return HttpResponseRedirect('/home')
        if not User.objects.get(username = sq):
            return HttpResponseRedirect('/home')
        doctor = USERMODEL.objects.get(name = sq)      
        return render(request,'home/docprof.html',{'type':doctor,'auth' : has_object_permission('authorised_doctor',request.user,User.objects.get(username = sq))})

@login_required()
#@has_role_decorator(['patient'])
@has_permission_decorator('view_doctors')
def doct(request):
    p = USERMODEL.objects.get(name = request.user.username)
    Users = User.objects.all()
    l = []
    for k in Users :
        if(has_object_permission('authorised_doctor',request.user,k)):
            z = USERMODEL.objects.get(name = k.username)
            l.append(z)
    return render(request,'home/docres.html',{'name':p.aname,'stuff':l})

@login_required()
def authorise_doc(request):
    if request.method =='GET':
        name = request.GET.get('doc_to_auth')
        try:
            q = USERMODEL.objects.get(name=name,type="Doctor")
        except:
            print("No such doctor exists")
            return
        q.legit_doctor = 1
        q.save()
        k = '/home/authorise?doc_to_auth='
        k = k+str(name)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseForbidden()

@login_required()
def grant(request):
    if request.method =='GET':
        name = request.GET.get('name')
        permission = request.GET.get('permission')
        grant_permission(User.objects.get(username = name),permission)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseForbidden()

@login_required()
def revoke(request):
    if request.method =='GET':
        name = request.GET.get('name')
        permission = request.GET.get('permission')
        revoke_permission(User.objects.get(username = name),permission)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseForbidden()
    
@login_required()
def revoke_all(request):
    if request.method =='GET':
        role = request.GET.get('role')
        permission = request.GET.get('permission')
        All = User.objects.all()
        for each in All:
            if(has_role(each,role) and not each.is_superuser):
                revoke_permission(each,permission)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseForbidden()

@login_required()
def remove(request):
    if request.method =='GET':
        name = request.GET.get('name')
        role = request.GET.get('role')
            
        try:
            q = User.objects.get(username=name)
        except:
            print("No such user exists")
            return HttpResponseRedirect('/home')

        Users = User.objects.all()
        if(not has_role(q,role) and not q.is_superuser):
            print("No such user of that role exists")
            return HttpResponseRedirect('/home')
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
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseForbidden()

@login_required()
def grant_all(request):
    if request.method =='GET':
        role = request.GET.get('role')
        permission = request.GET.get('permission')
        All = User.objects.all()
        for each in All:
            if(has_role(each,role) and not each.is_superuser):
                grant_permission(each,permission)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseForbidden()


@login_required()
def main(request):
    p = USERMODEL.objects.filter(name = request.user.username)
    first = USERMODEL.objects.filter(type="Doctor",legit_doctor = 0)
    second = USERMODEL.objects.all()
    third = ['view_forum','view_patients','upload_results','view_records','upload_pres','search','add_question','add_comment',
        'view_pres',
        'view_results',
        'schedule',
        'add_schedule',
        'delete_schedule',
        'upload_records',
        'authorize',
        'view_doctors']
    fourth = ["doctor","patient","public"]
    fifth = ["doctor","patient"]
    if(User.objects.get(username=request.user.username).is_superuser):
        return render(request,'home/admin.html',{'dropdown1':first,'dropdown2':second,'dropdown3':third,'dropdown4':fourth, 'dropdown5':fifth})
    if not p:
        return HttpResponseRedirect("/profile")
    k = USERMODEL.objects.get(name = request.user.username)
    if(k.legit_doctor == 1 and not has_role(request.user,'doctor')):
        assign_role(request.user,'doctor')
        k.auth = None
        k.save()
        k = USERMODEL.objects.get(name = request.user.username)

    if request.method == 'GET':
        sq = request.GET.get('search_box')
        if sq !=None and sq.strip() :
            z = USERMODEL.objects.filter(name__iexact = sq,type = "Doctor",legit_doctor = 1)
            f = USERMODEL.objects.filter(aname__iexact = sq,type = "Doctor", legit_doctor = 1)
            g = USERMODEL.objects.filter(phno__iexact = sq, type = "Doctor", legit_doctor = 1)
            n = USERMODEL.objects.filter(qual__iexact = sq, type = "Doctor", legit_doctor = 1)
            p = USERMODEL.objects.filter(aname__iexact = sq, type = "Doctor", legit_doctor = 1)
            j = USERMODEL.objects.filter(field__iexact = sq, type = "Doctor", legit_doctor = 1)
            p = z|f|g|n|p|j
            return render(request,'home/rend.html',{'query':p,'name':sq})

    return render(request,'home/PAt.html',{'name':k.aname})

