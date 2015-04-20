from django.conf.urls import patterns, include, url
from django.contrib import admin
from snakd.apps.chat import views as chatviews
from snakd.views import *

urlpatterns = patterns('',
    url(r'^', include('snakd.apps.user.urls')),
    url(r'^interest/', include('snakd.apps.interest.urls')),
    url(r'chat/', include('snakd.apps.chat.urls')),
    url(r'^', include('favicon.urls')),
    url(r'^.*', errorhandler, name="fourohfour"),
)
