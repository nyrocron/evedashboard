from django.conf.urls import patterns, url
from charmanager import views

urlpatterns = patterns('',
    url(r'^$', views.charList, name='list'),
    url(r'^add/$', views.charAdd, name='add'),
    url(r'^delete/(?P<pk>\d+)/$', views.charDelete, name='delete'),
)
