from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'UserInfo.views.users'),
	url(r'^password/', 'UserInfo.views.change_password'),
	url(r'^self[/]?$', 'UserInfo.views.profile'),
	url(r'^(?P<user>\w+)/$', 'UserInfo.views.single_user'),
)