from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'PartyList.views.parties'),
	url(r'^(?P<party>\w+)/?$', 'PartyList.views.partyguests'),
)
