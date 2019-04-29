from django.conf.urls import url, include
from django.contrib import admin

from.views import main,patup,upl

urlpatterns =[
url(r'^$',main),
url(r'^Patup$',patup),
url(r'^uploadpresc$',upl)
]
