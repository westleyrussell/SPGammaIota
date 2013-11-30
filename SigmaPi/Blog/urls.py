from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'Blog.views.index'),
	url(r'^(?P<slug>[\w-]+)/$', 'Blog.views.blog_post'),
)


    