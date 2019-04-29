from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from .views import showform


urlpatterns =[
url(r'^$',showform),

]
