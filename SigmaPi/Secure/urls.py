from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change

from Secure import views

urlpatterns = patterns('',
	url(r'^$', views.home, name="home"),
	url(r'^password/', password_change, {'template_name': 'reset_password.html', 'post_change_redirect' : views.home}),
	url(r'^archives/', include('Archives.urls')),
    url(r'^parties/', include('PartyList.urls')),
    url(r'^blog/', include('Blog.secure_urls')),
    url(r'^users/', include('UserInfo.secure_urls')),
)


    