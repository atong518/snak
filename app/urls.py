from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
    # splash page
    url(r'^$', views.splash, name='splash'),

    # sign up page
    url(r'^signup/$', views.sign_up, name='sign_up'),

    # how to page
    url(r'^howto/$', views.howto, name='howto'),
    # about us page
    url(r'^aboutus/$', views.aboutus, name='aboutus'),

    # login page
    url(r'^login/$', views.login, name='login'),

    # logout
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': 'login'}, name="logout"),

    # main/index page
    url(r'^main/$', views.main, name='main'),

<<<<<<< HEAD
    url(r'^interests/$', views.interests, name="interests"),

=======
    # user authentication pate
    url(r'^confirm_email/(?P<activation_code>\w+)/(?P<email>([a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)/', views.confirm_email, name="confirm_email"),
>>>>>>> cfde78248e9b1ae2394f170d2887c8e0f4e158f2
)
