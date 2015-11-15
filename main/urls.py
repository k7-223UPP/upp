from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
url(r'^$', 'main.views.home', name='main'),
)
