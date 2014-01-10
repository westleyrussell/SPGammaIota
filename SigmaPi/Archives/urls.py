from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = patterns('',
	url(r'^$', 'Archives.views.index'),
	url(r'^bylaws/$', 'Archives.views.bylaws'),
	url(r'^bylaws/delete/$', 'Archives.views.delete_bylaw'),
	url(r'^minutes/$', 'Archives.views.minutes'),
	url(r'^minutes/delete/$', 'Archives.views.delete_minutes'),
	url(r'^guides/$', 'Archives.views.guides'),
	url(r'^guides/delete/$', 'Archives.views.delete_guide'),
	url(r'^rules/$', 'Archives.views.rules'),
	url(r'^rules/delete/$', 'Archives.views.delete_rules'),
)
