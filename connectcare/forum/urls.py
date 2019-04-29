from django.conf.urls import url, include
from django.contrib import admin

from .views import question_list,question_detail,question_create,add_comment_to_post


urlpatterns=[
    url(r'^$',question_list,name='questions'),
    url(r'^create/$',question_create,name='create'),
    url(r'^(?P<id>\d+)/$',question_detail,name='detail'),
    url(r'^(?P<id>\d+)/comment/$', add_comment_to_post, name='add_comment_to_post'),

]

