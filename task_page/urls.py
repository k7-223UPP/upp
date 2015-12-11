from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns('',
    url(r'^(?P<id_section>[0-9]+)/(?P<id_task>[0-9]+)/$', views.task_page , name='task_page'),
    url(r'^close/(?P<id_section>[0-9]+)/(?P<id_task>[0-9]+)/$', views.task_page_close , name='task_page_close'),
)