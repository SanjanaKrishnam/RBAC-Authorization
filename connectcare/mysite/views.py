from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiledet.models import USERMODEL
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.conf import settings
# Create your views here.

def home(request):
    return render(request, 'mysite/home.html')
def register(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                try:
                    User.objects.create_user(username, email, password)
                    user = authenticate(username = username, password = password)
                    login(request, user)
                    return HttpResponseRedirect('/profile')
                except:
                    messages.info(request,'Invalid e-mail id')
                    form = UserRegistrationForm()
            else:
                messages.info(request,'Username or e-mail id has already been registered')
                form = UserRegistrationForm()
    else:
        form = UserRegistrationForm()
    return render(request, 'mysite/register.html', {'form' : form})
