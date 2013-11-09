from django.conf.urls import patterns, url

from UserInfo import views

urlpatterns = patterns('',
	url(r'^$', views.users, name="users"),
	url(r'^(?P<user>\w+)/$', views.single_user, name="single_user"),
	url(r'^self$', views.profile, name="self"),
)