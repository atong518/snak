from django.shortcuts import render
from snakd.apps.user.models import GenericUser, ProspieUser, CollegeUser
from snakd.apps.chat.models import Thread, Message

from snakd.apps.user.views import main

# Create your views here.
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
