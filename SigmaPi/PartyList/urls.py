from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'PartyList.views.parties'),
	url(r'^(?P<party>\w+)/guests$', 'PartyList.views.guests'),
	url(r'^(?P<party>\w+)/jobs$', 'PartyList.views.jobs'),
)
