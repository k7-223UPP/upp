from django.conf.urls import url, patterns


urlpatterns = patterns('',
    url(r'^$', "registration.views.registration", name='registration'),
)
