from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^login', 'django.contrib.auth.views.login'),
	url(r'^logout', 'django.contrib.auth.views.logout_then_login'),
	url(r'^$', 'Blog.views.index'),
	url(r'^history[/]$', 'PubSite.views.history'),
	url(r'^service[/]$', 'PubSite.views.service'),
	url(r'^blog/', include('Blog.urls')),
)