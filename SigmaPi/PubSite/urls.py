from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^login', 'django.contrib.auth.views.login'),
	url(r'^logout', 'django.contrib.auth.views.logout_then_login'),
	url(r'^$', 'PubSite.views.blog_index'),
	url(r'^history$', 'PubSite.views.history'),
	url(r'^service$', 'PubSite.views.service'),
	url(r'^blog[/]?$', 'PubSite.views.blog_index'),
	url(r'^blog/add/', 'PubSite.views.add_blog'),
	url(r'^blog/(?P<slug>[\w-]+)/$', 'PubSite.views.blog_post'),
	url(r'^blog/(?P<slug>[\w-]+)/edit/$', 'PubSite.views.edit_blog')
)