from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from snakd.apps.user.models import GenericUser
from snakd.apps.interest.models import Interest
from snakd.lib.orm import *
import json

def getUser(request):
	uid = request.session.get("_auth_user_id")
	user = GenericUser.objects.get(id=uid)
	return user

def makeInterestList(queryset):
	intlist = []
	for interest in queryset:
		intlist.append(interest.__str__())
	return intlist

def show(request):
	responsedict = {}
	responsedict["i_list"] = GetInterestTree()
	user = getUser(request)
	intlist = makeInterestList(user.interests.all())
	responsedict["user_interests"] = json.dumps(intlist)
	return render(request, 'interests/show.html', responsedict)


def update(request):
	import pdb; pdb.set_trace();
	interests = request.POST.get("interest_list");
	user = getUser(request)
	user.interests.clear()
	for interest in interests:
		intr = Interest.objects.filter(id=interest)
		user.interests.add(intr[0])

	user.save()
	return redirect(show)

