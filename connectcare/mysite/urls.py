from django.conf.urls import url, include
from django.contrib import admin
from .views import home,register
urlpatterns = [
    url(r'^register/$', register),
]
