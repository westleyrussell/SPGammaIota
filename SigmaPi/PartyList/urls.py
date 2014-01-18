from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'PartyList.views.index'),
	url(r'^add/', 'PartyList.views.add_party'),
	url(r'^manage/', 'PartyList.views.manage_parties'),
	url(r'^edit/(?P<party>\w+)/(?P<date>[0-9-]+)/$', 'PartyList.views.edit_party'),
	url(r'^delete/(?P<party>\w+)/(?P<date>[0-9-]+)/$', 'PartyList.views.delete_party'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/guests$', 'PartyList.views.guests'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/guests/create$', 'PartyList.api.create'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/guests/update/(?P<id>[0-9]+)$', 'PartyList.api.update'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/guests/destroy/(?P<id>[0-9]+)$', 'PartyList.api.destroy'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/guests/signIn/(?P<id>[0-9]+)$', 'PartyList.api.signin'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/guests/signOut/(?P<id>[0-9]+)$', 'PartyList.api.signout'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/guests/poll', 'PartyList.api.poll'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/guests/export', 'PartyList.api.export_list'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/jobs$', 'PartyList.views.jobs'),
	url(r'^(?P<party>\w+)/(?P<date>[0-9-]+)/count$', 'PartyList.api.updateCount'),
)
