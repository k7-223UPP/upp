__author__ = 'Anatoly'
from django.conf.urls import url, patterns
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'login.views.login', name='login'),
    url(r'^logout$', 'login.views.logout_view', name='logout'),
    url(r'^access$', 'login.views.access', name='access'),
    url(r'^process$', 'login.views.process', name='process'),
)
