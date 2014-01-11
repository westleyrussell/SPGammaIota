from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = patterns('',
	url(r'^$', 'Links.views.view_all'),
	url(r'^visit/(?P<link>[\d]+)/$', 'Links.views.visit_link'),
	url(r'^add/$', 'Links.views.add_link'),
	url(r'^(?P<link>[\d]+)/comment/$', 'Links.views.add_comment'),
	url(r'^(?P<link>[\d]+)/like/$', 'Links.views.change_like')

)
