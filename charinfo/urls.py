from django.conf.urls import patterns, url

from charinfo import views

urlpatterns = patterns('',
    url(r'^$', views.charList, name='list'),
    url(r'^detail/(?P<pk>\d+)/$', views.charDetail, name='detail'),
    url(r'^tile/(?P<pk>\d+)/$', views.charTile, name='tile'),
)