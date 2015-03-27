from django.conf.urls import patterns, include, url
from django.contrib import admin
from snakd.apps.chat import views as chatviews

urlpatterns = patterns('',
    url(r'^$', chatviews.chat, name='chat'),
    url(r'^send_chat_message/$', chatviews.send_chat_message, name="send_chat_message"),
    url(r'^check_for_new_messages/$', chatviews.check_for_new_messages, name="check_for_new_messages"),
    url(r'^add_user_to_thread/$', chatviews.add_user_to_thread, name="add_user_to_thread"),
    url(r'^leave_thread/$', chatviews.leave_thread, name="leave_thread"),
    url(r'^new_thread/$', chatviews.new_thread, name="new_thread"),
)