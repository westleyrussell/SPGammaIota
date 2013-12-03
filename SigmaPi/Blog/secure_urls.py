from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^$', 'Blog.views.secure_index'),
	url(r'^add/', 'Blog.views.add_blog'),
	url(r'^delete/', 'Blog.views.delete_blog'),
	url(r'^(?P<slug>[\w-]+)/$', 'Blog.views.edit_blog')
)


    