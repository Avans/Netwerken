from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'views.home'),
    url(r'^weather$', 'views.weather'),
    url(r'^quote$', 'views.quote'),
)
