from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'Standards.views.index'),
	url(r'^bones/$', 'Standards.views.edit_bones'),
	url(r'^points/$', 'Standards.views.edit_points'),
	url(r'^points/request/$', 'Standards.views.request_points'),
)
