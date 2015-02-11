import json
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from snakd.apps.user.models import GenericUser, ProspieUser, CollegeUser
from snakd.apps.chat.models import Thread, Message

from snakd.apps.user.views import main

def chat(request):
    # get logged in user id
    if not request.user.is_authenticated():
        return redirect(main)

    user_pk = request.user.pk

    # get all threads the user is involved in
    inbox = Thread.objects.filter(members__id=user_pk)
    
    # get all messages associated with first thread
    first_thread = inbox.first() #GET RID OF THIS ITS STUPID
    messages = Message.objects.filter(thread=first_thread)
    return render(request,
                  'messages/chat.html',
                  {'inbox_threads' : inbox,
                   'messages' : messages})

def send_chat_message(request):
#    import pdb; pdb.set_trace();
    if request.method == 'POST':
        text = request.POST.get('message_text')
        thread_id = request.POST.get('thread_id')
        response_data = {}
        thread = get_object_or_404(Thread, pk=thread_id)
        message = Message(text=text, sender=request.user, thread=thread)
        message.save()

        response_data["result"] = "message sent successfully!"
        response_data["message_pk"] = message.pk
        response_data["text"] = message.text

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")

#        return HttpResponse(
#            json.dumps(response_data),
#            content_type="application/json"
#        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json")
