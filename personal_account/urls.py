from django.conf.urls import url, patterns

urlpatterns = patterns('',
url(r'^$', 'personal_account.views.private_data', name='private_data'),
                       )
