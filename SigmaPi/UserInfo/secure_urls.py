from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^$', 'UserInfo.views.manage_users'),
	url(r'^add/', 'UserInfo.views.add_users'),
	url(r'^edit/(?P<user>\w+)/$', 'UserInfo.views.edit_user'),
	url(r'^reset_password/(?P<user>\w+)/$', 'UserInfo.views.reset_password'),
)


    