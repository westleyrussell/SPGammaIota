from django.conf.urls import patterns, include, url

from Secure import views

urlpatterns = patterns('',
	url(r'^$', views.home, name="home"),
	url(r'^archives/', include('Archives.urls')),
    url(r'^parties/', include('PartyList.urls')),
    url(r'^blog/', include('Blog.secure_urls')),
    url(r'^users/', include('UserInfo.secure_urls')),
    url(r'^library/', include('Library.secure_urls')),
    url(r'^links/', include('Links.urls')),
    url(r'^standards/', include('Standards.urls'))
)



