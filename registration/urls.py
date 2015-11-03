from django.conf.urls import url, patterns


urlpatterns = patterns('',
    url(r'^$', "registration.views.registration", name='registration'),
    url(r'^regs/', "registration.views.regs", name='regs')
)
