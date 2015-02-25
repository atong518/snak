import json
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from snakd.apps.user.models import GenericUser, ProspieUser, CollegeUser
from snakd.apps.chat.models import Thread, Message

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
#    import pdb; pdb.set_trace()
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
#    import pdb; pdb.set_trace();
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
#    import pdb; pdb.set_trace();
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
        
