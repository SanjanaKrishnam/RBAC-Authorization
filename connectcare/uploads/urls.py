from django.conf.urls import url, include
from django.contrib import admin

from.views import upl,home

urlpatterns =[
url(r'^$',home),
url(r'^uploads$',upl),
]
