from django.conf.urls import patterns, url

from PubSite import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^logout/', views.logout_view, name='logout_view'),
    url(r'^login/', views.login_view, name='login_view')
)