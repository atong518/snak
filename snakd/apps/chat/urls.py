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
    url(r'^refer_friend/$', chatviews.refer_friend, name="refer_friend"),
    url(r'^report_person/$', chatviews.report_person, name="report_person"),
    url(r'^nudge_person/$', chatviews.nudge_person, name="nudge_person"),
    url(r'^submit_feedback/$', chatviews.submit_feedback, name="submit_feedback"),
    url(r'^reset_counter/$', chatviews.reset_counter, name="reset_counter"),
)
