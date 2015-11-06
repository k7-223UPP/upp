from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('',
url(r'^$', 'personal_account.views.personal_account', name='personal_account'),
url(r'^private_data$', 'personal_account.views.private_data', name='private_data'),
)
