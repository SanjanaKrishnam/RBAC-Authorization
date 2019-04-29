from django.conf.urls import url, include
from django.contrib import admin

from .views import main, testup, docfin

urlpatterns =[
url(r'^$',main),
url(r'^testup',testup),
url(r'^uploadtest',docfin),
]
