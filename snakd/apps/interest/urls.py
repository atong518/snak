from django.conf.urls import patterns, url

from snakd.apps.interest import views

urlpatterns = patterns('snakd.apps.interest',

    url(r'^show/$', views.show, name="show"),

)
