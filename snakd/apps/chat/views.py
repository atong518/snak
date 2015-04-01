import json
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from snakd.apps.user.models import GenericUser, ProspieUser, CollegeUser
from snakd.apps.chat.models import Thread, Message
from snakd.apps.user.models import GenericUser

from snakd.apps.user.views import login

def chat(request):
    # get logged in user id
    if not request.user.is_authenticated():
        return redirect(login)

    user_pk = request.user.pk

    # get all threads the user is involved in
    inbox = Thread.objects.filter(members__id=user_pk)
    
    # get all users matched with the logged-in user
    matched_users = GenericUser.objects.all() #CHANGE THIS ONCE WE HAVE A WAY TO GET MATCHED USERS

    return render(request,
                  'messages/chat.html',
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
        
def new_thread(request):
    # TODO: Where do we get the subject?
    try:
        uid = request.session.get("_auth_user_id")
        user1 = GenericUser.objects.get(id=uid)        
        dic = request.POST.dict()
        user2 = GenericUser.objects.get(id=dic['otherid'])
        newthread = Thread()
        newthread.save()
        newthread.members.add(user1)
        newthread.members.add(user2)
        m = Message(thread=newthread, text=dic['message'], sender=user1)
        m.save()
        return HttpResponse(
            json.dumps({"ignore": "this isn't happening"}),
            content_type="application/json")
    except:
        pass

def refer_friend(request):
    # Send referral email
    if request.method == "POST" and request.user.is_authenticated():
        email = request.POST.get("refer-email")
        subject = "Want to know what it's like to go to Dartmouth College?"

        referer_name = request.user.firstname + " " + request.user.lastname

        message = "Hi " + request.POST.get("refer-name") + "!\n"
        message += "Are you interested in going to Dartmouth College?  Do you want to find out what it's like to be a student here?\n"
        message += 'At Sagely, we help prospective Dartmouth students like you get an "inside look" into what it\'s like to go to Dartmouth. We help you get personalized answers to your questions by connecting you directly with real Dartmouth students.\n'
        message += referer_name + " thought thought you might be interested in using Sagely and told us to get in touch with you! We Dartmouth students would love nothing more than to share our experiences, so give us a shot and check us out "
        message += "at www.sagely.io!\n"
        message += "Cheers!\nThe Sagely Team"

        html_message = "<h3>Hi " + request.POST.get("refer-name") + "!</h3>"
        html_message += "<p>Are you interested in going to Dartmouth College?  Do you want to find out what it's like to be a student here?</p>"
        html_message += '<p>At Sagely, we help prospective Dartmouth students like you get an "inside look" into what it\'s like to go to Dartmouth. We help you get personalized answers to your questions by connecting you directly with real Dartmouth students.</p>'
        html_message += "<p>" + referer_name + " thought you might be interested in using Sagely and told us to get in touch with you! We Dartmouth students would love nothing more than to share our experiences, so give us a shot and check us out "
        html_message += '<a href="www.sagely.io">here</a>!'
        html_message += "<p>Cheers!</p><p><b>The Sagely Team</b></p>"

        from_email = settings.EMAIL_HOST_USER
        
        msg = EmailMultiAlternatives(subject, message, from_email, {email})
        msg.attach_alternative(html_message, "text/html")
        msg.send()

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

    return redirect(chat)

def submit_feedback(request):
    # Submit feedback
    if request.method == "POST":
        issue = request.POST.get("send-feedback-text")
        subject = "FEEDBACK RECEIVED"
        message = "Submitted by: " + request.user.firstname + " " + request.user.lastname
        message += " (email: " + request.user.email + ")\n"
        message += "\nIssue: " + issue
        from_email = settings.EMAIL_HOST_USER

        html_message = "<h3>REPORT RECEIVED</h3>"
        html_message += "<p><b>Submitted by</b>: " + request.user.firstname + " " + request.user.lastname + " (" + request.user.email + ")</p>"
        html_message += "<p><b>Issue</b>: " + issue

        # TODO: Should we send a copy of the email to the person who reported it as well?
        msg = EmailMultiAlternatives(subject, message, from_email, {from_email})
        msg.attach_alternative(html_message, "text/html")
        msg.send()

    return redirect(chat)
