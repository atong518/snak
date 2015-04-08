import json
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib import messages
from snakd.apps.user.models import GenericUser, ProspieUser, CollegeUser
from snakd.apps.chat.models import Thread, Message
from snakd.apps.user.models import GenericUser
from datetime import datetime, timedelta, date

from snakd.apps.user.views import login

def sortInbox(inbox):
    for thread in range(len(inbox)-1,0,-1):
        for i in range(thread):
            import pdb; pdb.set_trace()
            if inbox[i].mostRecentMessage() >inbox[i+1].mostRecentMessage():
                temp = inbox[i]
                inbox[i] = inbox[i+1]
                inbox[i+1] = temp
    import pdb; pdb.set_trace()
    return inbox


def chat(request):
    # get logged in user id
    if not request.user.is_authenticated():
        return redirect(login)

    user_pk = request.user.pk

    # get all threads the user is involved in
    # inbox = Thread.objects.filter(members__id=user_pk, order_by=)
    # inbox = Thread.objects.filter(members__id=user_pk)
    # inbox = sortInbox(inbox)
    inbox = Thread.objects.in_a_number_order(members__id=user_pk)
    # get all users matched with the logged-in user
    matched_users = GenericUser.objects.all() # TODO CHANGE THIS ONCE WE HAVE A WAY TO GET MATCHED USERS

    # message_text = "debug"
    # messages.add_message(request, messages.INFO, message_text, fail_silently=True)
    
    # Nudge person logic
    if request.method == "POST" and request.POST.get("reported-name") and request.POST.get("selected-thread-id"):
        # get user email
        threadId = request.POST.get("selected-thread-id")
        thread = Thread.objects.get(pk=threadId)
        firstname = request.POST.get("reported-name").split(" ")[0]
        lastname = request.POST.get("reported-name").split(" ")[1]
        nudgedUser = thread.members.filter(firstname=firstname, lastname=lastname).first()
        # if last message sent by nudgedUser in this thread (or if they haven't sent a message
        # in this thread) is > 5 days ago, and nudgedUser last_nudged is > 5 days ago, send 
        # email to nudgedUser.email

        message_text = "Thanks for letting us know! We've nudged " + firstname + " for you!"

        # look at snakd/apps/chat/models.py
        # use thread to get number of members, disable if >2
        # get last message time from thread.mostRecentMessage and compare sent_at with datetime.now()

        # NO MORE GROUP CHATS
        # need a thread model function to return last sent message,
        # compare message to sender, only send nudge if they're the same
        # fix thread user list?

        # if last message is fewer than 5 days old, display wait message and don't send email
        if thread.mostRecentMessage() > (date.today() - timedelta(days=5)):
            message_text = "Let's give " + firstname + " a little more time to answer!"
        else:
            issue = request.POST.get("report-issue-text")
            subject = "REPORT RECEIVED"
            message = "Reported by: " + request.user.firstname + " " + request.user.lastname
            message += " (email: " + request.user.email + ")\n"
            message += "Reported on: " + request.POST.get("reported-name")
            message += "\nIssue: " + issue
            from_email = settings.EMAIL_HOST_USER

            html_message = "<h3>REPORT RECEIVED</h3>"
            html_message += "<p><b>Reported by</b>: " + request.user.firstname + " " + request.user.lastname + " (" + request.user.email + ")</p>"
            html_message += "<p><b>Reported on</b>: " + request.POST.get("reported-name") + "</p>"
            html_message += "<p><b>Issue</b>: " + issue

            # TODO: Should we send a copy of the email to the person who reported it as well?
            msg = EmailMultiAlternatives(subject, message, from_email, {from_email})
            msg.attach_alternative(html_message, "text/html")
            msg.send()

        
        messages.add_message(request, messages.INFO, message_text, fail_silently=True)

    return render(request, 'messages/chat.html',
                  {'inbox_threads' : inbox,
                   'matched_users' : matched_users})

def check_for_new_messages(request):
    if request.method == 'POST' and len(request.POST.get('thread_id')) > 0:
        thread_id = request.POST.get('thread_id')
        response_data = []
        thread = get_object_or_404(Thread, pk=thread_id)
        
        messages = thread.message_set.all()
        for message in messages:
            response_data.append([message.text, message.sender.email])

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"ignore": "this isn't happening"}),
            content_type = "application/json")

def send_chat_message(request):
    if request.method == 'POST' and len(request.POST.get('message_text')) > 0:
        text = request.POST.get('message_text')
        thread_id = request.POST.get('thread_id')
        response_data = {}
        thread = get_object_or_404(Thread, pk=thread_id)
        message = Message(text=text, sender=request.user, thread=thread)
        message.save()

        response_data["result"] = "message sent successfully!"
        response_data["message_pk"] = message.pk
        response_data["text"] = message.text
        response_data["sender"] = message.sender.email

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")

    else:
        return HttpResponse(
            json.dumps({"ignore": "this isn't happening"}),
            content_type="application/json")

def add_user_to_thread(request):
    if request.method == 'POST' and len(request.POST.get('user_email')) > 0:
        user_email = request.POST.get('user_email')
        thread_id = request.POST.get('thread_id')
        response_data = {}
        thread = get_object_or_404(Thread, pk=thread_id)
        user = get_object_or_404(GenericUser, email=user_email)
        thread.members.add(user)
        thread.save()

        response_data["result"] = "user added successfully!"
        response_data["new_user_name"] = user.firstname + " " + user.lastname

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")

    else:
        return HttpResponse(
            json.dumps({"ignore": "this isn't happening"}),
            content_type="application/json")

def leave_thread(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        thread_id = request.POST.get('thread_id')
        user = get_object_or_404(GenericUser, email=user_email)
        thread = get_object_or_404(Thread, pk=thread_id)
        thread.members.remove(user)
        thread.save()

    return HttpResponse(
        json.dumps({"ignore": "this isn't happening"}),
        content_type="application/json")


def _send_match_notification(user, match):
    try:
        if isinstance(user, CollegeUser):
            subject = "Meet your Sage(ly)!"
        else:
            subject = "Ready to give Sagely advice?"
        message = "Hi " + match.firstname + ",<br><br>"
        message += "Great news, you got matched with " + user.firstname + "!<br><br>"
        if match.interests.all():
            message += "They're interested in the following:<br>"
            for interest in match.interests.all():
                message += "   - " + interest.name + "<br>"
            message += "<br>"
        message += "Head here to respond, sagely.io, " + user.firstname + " is waiting ;)<br><br>"
        message += "The Sagely Team"
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(subject, message, from_email, {match.email})
        msg.attach_alternative(message, "text/html")
        msg.send()
    except:
        pass

def _specify_class(user):
    try:
        user = user.collegeuser
    except:
        user = user.prospieuser
    return user

def new_thread(request):
    # TODO: Where do we get the subject?
    try:
        uid = request.session.get("_auth_user_id")
        user1 = GenericUser.objects.get(id=uid)  
        dic = request.POST.dict()
        user2 = GenericUser.objects.get(id=dic['otherid'])
        user1 = _specify_class(user1)      
        user2 = _specify_class(user2)      
        if isinstance(user1, CollegeUser):
            c_user = user1
        else:
            c_user = user2
        user1.matches.add(user2)
        _send_match_notification(user1, user2)
        c_user.next_match = (
            datetime.now() + 
            timedelta(days=c_user.max_match_frequency)
        )

        newthread = Thread()
        newthread.save()
        newthread.members.add(user1)
        newthread.members.add(user2)
        m = Message(thread=newthread, text=dic['message'], sender=user1)
        m.save()
        return HttpResponse(
            json.dumps({"threadid": newthread.id}),
            content_type="application/json")
    except:
        pass

def refer_friend(request):
    # Send referral email
    if request.method == "POST" and request.user.is_authenticated():
        email = request.POST.get("refer-email")
        subject = "Want to know what it's like to go to Dartmouth College?"

        referer_name = request.user.firstname + " " + request.user.lastname

        message = "Hi " + request.POST.get("refer-name") + '''!
                   Are you interested in going to Dartmouth College?  Do you want to find out what it's like to be a student here?
                   At Sagely, we help prospective Dartmouth students like you get an "inside look" into what it's like to go to Dartmouth. We help you get personalized answers to your questions by connecting you directly with real Dartmouth students.
             ''' + referer_name + ''' thought thought you might be interested in using Sagely and told us to get in touch with you! We Dartmouth students would love nothing more than to share our experiences, so give us a shot and check us out at www.sagely.io!
                   Cheers!
                   The Sagely Team'''

        html_message =  "<h3>Hi " + request.POST.get("refer-name") + '''!</h3>
                        <p>Are you interested in going to Dartmouth College?  Do you want to find out what it's like to be a student here?</p>
                        <p>At Sagely, we help prospective Dartmouth students like you get an "inside look" into what it's like to go to Dartmouth. We help you get personalized answers to your questions by connecting you directly with real Dartmouth students.</p>
                        <p>''' + referer_name + ''' thought you might be interested in using Sagely and told us to get in touch with you! We Dartmouth students would love nothing more than to share our experiences, so give us a shot and check us out <a href="www.sagely.io">here</a>!</p>
                        <p>Cheers!</p><p><b>The Sagely Team</b></p>'''

        from_email = settings.EMAIL_HOST_USER
        
        msg = EmailMultiAlternatives(subject, message, from_email, {email})
        msg.attach_alternative(html_message, "text/html")
        msg.send()

        message_text = "Thanks for spreading the Sagely love! We just got in touch with " + request.user.firstname + ". :)"
        messages.add_message(request, messages.INFO, message_text, fail_silently=True)

    return redirect(chat)

def report_person(request):
    # Send report on person
    if request.method == "POST":
        issue = request.POST.get("report-issue-text")
        subject = "REPORT RECEIVED"
        message = "Reported by: " + request.user.firstname + " " + request.user.lastname
        message += " (email: " + request.user.email + ")\n"
        message += "Reported on: " + request.POST.get("reported-name")
        message += "\nIssue: " + issue
        from_email = settings.EMAIL_HOST_USER

        html_message = "<h3>REPORT RECEIVED</h3>"
        html_message += "<p><b>Reported by</b>: " + request.user.firstname + " " + request.user.lastname + " (" + request.user.email + ")</p>"
        html_message += "<p><b>Reported on</b>: " + request.POST.get("reported-name") + "</p>"
        html_message += "<p><b>Issue</b>: " + issue

        # TODO: Should we send a copy of the email to the person who reported it as well?
        msg = EmailMultiAlternatives(subject, message, from_email, {from_email})
        msg.attach_alternative(html_message, "text/html")
        msg.send()

        message_text = "Thanks for letting us know. We're on it!"
        messages.add_message(request, messages.INFO, message_text, fail_silently=True)

    return redirect(chat)

def submit_feedback(request):
    # Submit feedback
    if request.method == "POST":
        issue = request.POST.get("send-feedback-text")
        subject = "FEEDBACK RECEIVED"
        message = "Submitted by: " + request.user.firstname + " " + request.user.lastname
        message += " (email: " + request.user.email + ")\n"
        message += "\nFeedback: " + issue
        from_email = settings.EMAIL_HOST_USER

        html_message = "<h3>REPORT RECEIVED</h3>"
        html_message += "<p><b>Submitted by</b>: " + request.user.firstname + " " + request.user.lastname + " (" + request.user.email + ")</p>"
        html_message += "<p><b>Issue</b>: " + issue

        msg = EmailMultiAlternatives(subject, message, from_email, {from_email})
        msg.attach_alternative(html_message, "text/html")
        msg.send()

        message_text = "Thanks for your thoughts! We really appreciate it!"
        messages.add_message(request, messages.INFO, message_text, fail_silently=True)

    return redirect(chat)
