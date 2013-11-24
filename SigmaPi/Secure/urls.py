from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from Secure import views

urlpatterns = patterns('',
	url(r'^$', views.home, name="home"),
	url(r'^archives/', include('Archives.urls')),
    url(r'^parties/', include('PartyList.urls')),
)


    