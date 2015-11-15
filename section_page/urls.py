from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^(?P<section_id>[0-9]+)/$', "section_page.views.section_page", name='section_page')
)
