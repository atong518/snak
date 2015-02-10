from django.conf.urls import patterns, include, url
from django.contrib import admin
from snakd.apps.chat import views as chatviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'snakd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('snakd.apps.user.urls')),
    url(r'^interest/', include('snakd.apps.interest.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^messages/', include("postman.urls")),

    url(r'^chat/$', chatviews.chat, name='chat'),

)
