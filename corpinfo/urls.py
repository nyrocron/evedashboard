from django.conf.urls import patterns, url

from corpinfo import views

urlpatterns = patterns('',
    url(r'^$', views.corpList, name='list'),
    url(r'^contracts/(?P<pk>\d+)/$', views.corpContracts, name='contracts'),
)
