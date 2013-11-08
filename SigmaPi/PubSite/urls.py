from django.conf.urls import patterns, url

from PubSite import views

urlpatterns = patterns('',
	url(r'', 'django.contrib.auth.views.login',name="login")
)