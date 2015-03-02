from django.conf.urls import patterns, url

from snakd.apps.user import views

urlpatterns = patterns('',
    # splash page
    url(r'^$', views.splash, name='splash'),

    # sign up page
    url(r'^signup/$', views.sign_up, name='sign_up'),

    # change password page
    url(r'^change_password/$', views.change_password, name='change_password'),

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

    # user authentication page
    url(r'^confirm_email/(?P<activation_code>\w+)/(?P<email>([a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)/', views.confirm_email, name="confirm_email"),

    url(r'^settings/$', views.edit, name='settings'),

    url(r'^match/$', views.match, name='match'),
)
