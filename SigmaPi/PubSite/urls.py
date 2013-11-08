from django.conf.urls import patterns, url

from PubSite import views

urlpatterns = patterns('',
	url(r'^login/', 'django.contrib.auth.views.login',name="login"),
	url(r'^logout/', 'django.contrib.auth.views.logout_then_login',name="logout"),
	url(r'^', views.index, name="index"),

)