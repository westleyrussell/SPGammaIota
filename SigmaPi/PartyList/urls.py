from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'PartyList.views.index'),
	url(r'^(?P<party>\w+)/guests$', 'PartyList.views.guests'),
	url(r'^(?P<party>\w+)/guests/create$', 'PartyList.api.create'),
	url(r'^(?P<party>\w+)/guests/update/(?P<id>[0-9]+)$', 'PartyList.api.update'),
	url(r'^(?P<party>\w+)/guests/destroy/(?P<id>[0-9]+)$', 'PartyList.api.destroy'),
	url(r'^(?P<party>\w+)/guests/signIn/(?P<id>[0-9]+)$', 'PartyList.api.signin'),
	url(r'^(?P<party>\w+)/guests/signOut/(?P<id>[0-9]+)$', 'PartyList.api.signout'),
	url(r'^(?P<party>\w+)/guests/poll', 'PartyList.api.poll'),
	url(r'^(?P<party>\w+)/jobs$', 'PartyList.views.jobs'),
	url(r'^(?P<party>\w+)/count$', 'PartyList.api.updateCount'),
)
