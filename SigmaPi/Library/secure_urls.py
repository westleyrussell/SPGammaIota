from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'Library.views.main', name='main'),
)
