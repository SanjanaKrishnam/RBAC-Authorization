from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
   url(r'^$', main),
   url(r'docprof$',doc),
   url(r'auth$',auth),
   url(r'docts$',doct),
   url(r'pat$',pat),
   url(r'authorise$',authorise_doc),
   url(r'grant$',grant),
   url(r'revoke$',revoke),
   url(r'revoke_all$',revoke_all),
   url(r'grant_all$',grant_all),
   url(r'remove$',remove)
]
