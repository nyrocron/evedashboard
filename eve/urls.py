from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eve.views.home', name='home'),
    # url(r'^eve/', include('eve.foo.urls')),

    url(r'^charinfo/', include('charinfo.urls', namespace="charinfo")),
    url('^accounts/', include('django.contrib.auth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
