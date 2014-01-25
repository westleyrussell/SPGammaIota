from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'Philanthropy.views.index'),
	url(r'^hours/$', 'Philanthropy.views.manage_hours'),
	url(r'^hours/(?P<brother>[\d]+)/$', 'Philanthropy.views.add_hours'),
	url(r'^hours/request/$', 'Philanthropy.views.request_hours'),
	url(r'^hours/request/(?P<hoursreq>[\d]+)/delete/$', 'Philanthropy.views.delete_request'),
	url(r'^hours/request/(?P<hoursreq>[\d]+)/accept/$', 'Philanthropy.views.accept_request'),
	url(r'^hours/reset/$', 'Philanthropy.views.reset_hours'),
)