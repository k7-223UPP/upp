__author__ = 'Anatoly'
from django.conf.urls import url, patterns
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'login.views.login', name='login'),
)
