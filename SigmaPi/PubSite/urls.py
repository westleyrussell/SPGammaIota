from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from PubSite import views

urlpatterns = patterns('',
	url(r'^login', 'django.contrib.auth.views.login',name="login"),
	url(r'^logout', 'django.contrib.auth.views.logout_then_login',name="logout"),
	url(r'^$', views.blog_index, name="index"),
	url(r'^history$', views.hisotry, name="history"),
	url(r'^service$', views.service, name="service"),
	url(r'^blog[/]?$', views.blog_index),
	url(r'^blog/(?P<path>\w+)/$', views.blog_post, name="index")
)