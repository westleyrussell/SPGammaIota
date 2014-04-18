from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
	url(r'^$', 'Archives.views.index'),

	# Bylaws
	url(r'^bylaws/$', 'Archives.views.bylaws'),
	url(r'^bylaws/(?P<bylaw>[\d]+)/$', 'Archives.views.download_bylaw'),
	url(r'^bylaws/delete/$', 'Archives.views.delete_bylaw'),

	# Meeting minutes
	url(r'^minutes/$', 'Archives.views.minutes'),
	url(r'^minutes/delete/$', 'Archives.views.delete_minutes'),
	url(r'^minutes/(?P<minutes>[\d]+)/$', 'Archives.views.download_minutes'),

	# House guides
	url(r'^guides/$', 'Archives.views.guides'),
	url(r'^guides/delete/$', 'Archives.views.delete_guide'),
	url(r'^guides/(?P<guides>[\d]+)/$', 'Archives.views.download_guides'),

	# House rules
	url(r'^rules/$', 'Archives.views.rules'),
	url(r'^rules/delete/$', 'Archives.views.delete_rules'),
	url(r'^rules/(?P<rules>[\d]+)/$', 'Archives.views.download_rules'),
)
