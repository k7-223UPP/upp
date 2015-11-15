from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^$', "sectionlist.views.sectionlist", name='sectionlist'),

)
