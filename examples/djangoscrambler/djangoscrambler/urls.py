from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'scramble.views.index', name='index'),
)
