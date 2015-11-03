from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('',
url(r'^$', 'main.views.home', name='main'),
)
