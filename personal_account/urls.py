from django.conf.urls import url, patterns

urlpatterns = patterns('',
url(r'^$', 'personal_account.views.private_data', name='private_data'),
url(r'^submissions$', 'personal_account.views.submissions', name='submissions'),
url(r'^general_statistics$', 'personal_account.views.general_statistics', name='general_statistics'),
url(r'^section_statistics/(?P<section_id>[0-9]+)/$', 'personal_account.views.section_statistics', name='section_statistics')
                       )
