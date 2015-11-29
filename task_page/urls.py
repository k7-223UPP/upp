from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns('',
    url(r'^(?P<userPT_ID>[0-9]+)/(?P<section_ID>[0-9]+)/(?P<user_ID>[0-9]+)/(?P<task_ID>[0-9]+)/$', views.task_page , name='task_page')
)
