from django.conf.urls import patterns, include, url
from django.contrib import admin
from snakd.apps.chat import views as chatviews

urlpatterns = patterns('',
    url(r'^', include('snakd.apps.user.urls')),
    url(r'^interest/', include('snakd.apps.interest.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # url(r'^messages/', include("postman.urls")),

    # chat urls - TODO: move these to a chat urls.py file if this gets too cluttered
    url(r'^chat/$', chatviews.chat, name='chat'),
    url(r'^chat/send_chat_message/$', chatviews.send_chat_message, name="send_chat_message"),
    url(r'^chat/check_for_new_messages/$', chatviews.check_for_new_messages, name="check_for_new_messages"),
)
