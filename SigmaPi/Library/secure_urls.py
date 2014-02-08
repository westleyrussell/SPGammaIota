from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'Library.views.main', name='main'),
	url(r'^library/(?P<scan_index>[\d]+)/$', 'Library.views.download_testscan'),
)
