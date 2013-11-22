from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from PubSite import views

urlpatterns = patterns('',
	url(r'^archives/', include('Archives.urls')),
    url(r'^parties/', include('PartyList.urls')),
)


    