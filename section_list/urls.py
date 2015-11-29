from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^$', "section_list.views.sectionlist", name='section_list'),

)
