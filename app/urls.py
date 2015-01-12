from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
    # splash page
    url(r'^$', views.splash, name='splash'),
    # sign up page
    url(r'^signup/$', views.sign_up, name='sign_up'),
)
