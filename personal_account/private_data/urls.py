from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
url(r'^', 'personal_account.private_data.views.private_data', name='private_data'),
)
