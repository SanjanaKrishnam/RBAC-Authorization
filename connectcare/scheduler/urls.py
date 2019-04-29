from django.conf.urls import url, include
from django.contrib import admin

from .views import scheduler,add_appointment_form,delete_appointment,appointment_form


urlpatterns=[
    url(r'^$',scheduler,name='scheduler'),
    url(r'^add_appointment/$',add_appointment_form, name='add_appointment'),
    url(r'^delete_appointment/(\d+)/$', delete_appointment, name='delete_appointment'),
    url(r'^edit_appointment/(\d+)?/$', appointment_form, name='edit_appointment'),
]
