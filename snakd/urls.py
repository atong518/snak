from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'snakd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('snakd.apps.app.urls')),

    url(r'^admin/', include(admin.site.urls)),

#    url(r'^/signup$', inclu
)
