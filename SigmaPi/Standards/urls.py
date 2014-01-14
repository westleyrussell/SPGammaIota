from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'Standards.views.index'),
	url(r'^bones/$', 'Standards.views.edit_bones'),
	url(r'^bones/(?P<bone>[\d]+)/$', 'Standards.views.edit_bone'),
	url(r'^bones/(?P<bone>[\d]+)/expire/$', 'Standards.views.expire_bone'),
	url(r'^bones/add/', 'Standards.views.add_bone'),
	url(r'^bones/probation/add/', 'Standards.views.add_probation'),
	url(r'^bones/probation/(?P<probation>[\d]+)/delete', 'Standards.views.end_probation'),
	url(r'^points/$', 'Standards.views.edit_points'),
	url(r'^points/(?P<brother>[\d]+)/$', 'Standards.views.add_points'),
	url(r'^points/request/$', 'Standards.views.request_points'),
)
