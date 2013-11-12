from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = patterns('',
	url(r'^$', 'Archives.views.index'),
	url(r'^bylaws/$', 'Archives.views.bylaws'),
	url(r'^bylaws/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/?$', 'Archives.views.single_bylaw'),
	url(r'^minutes/$', 'Archives.views.minutes'),
	url(r'^minutes/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/?$', 'Archives.views.single_minutes'),
	url(r'^guides/$', 'Archives.views.guides'),
	url(r'^guides/(?P<path>\w+)/$', 'Archives.views.single_guide'),
	url(r'^rules/$', 'Archives.views.rules'),
	url(r'^rules/(?P<path>\w+)/$', 'Archives.views.single_rule'),
)
