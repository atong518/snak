from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
    # splash page
    url(r'^$', views.splash, name='splash'),

)
