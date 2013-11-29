from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'PartyList.views.index'),
	url(r'^(?P<party>\w+)/guests$', 'PartyList.views.guests'),
	url(r'^(?P<party>\w+)/guests/create$', 'PartyList.api.create'),
	url(r'^(?P<party>\w+)/guests/update$', 'PartyList.api.update'),
	url(r'^(?P<party>\w+)/guests/destroy$', 'PartyList.api.destroy'),
	url(r'^(?P<party>\w+)/guests/poll$', 'PartyList.api.poll'),
	url(r'^(?P<party>\w+)/jobs$', 'PartyList.views.jobs'),
)
