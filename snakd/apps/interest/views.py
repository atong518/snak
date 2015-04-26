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
		intlist.append(interest.get_kwargs())
	return intlist

def getInterestNames():
	dict_of_names = []
	for interest in Interest.objects.all():
		if interest.name != "HEAD":
			dict_of_names.append({"name": interest.name, "id": interest.id})
	return dict_of_names

def getInterestStrings():		
	list_of_names = ""
	for interest in Interest.objects.all():
		if interest.name != "HEAD":
			list_of_names += interest.name + ", "
	return list_of_names[:-2]

def show(request):
	responsedict = {}
	responsedict["i_list"] = GetInterestTree()
	responsedict["all_interests"] = getInterestNames()
	responsedict["all_interests_string"] = getInterestStrings()
	user = getUser(request)
	intlist = makeInterestList(user.interests.all())
	responsedict["user_interests"] = json.dumps(intlist)
	return render(request, 'interests/show.html', responsedict)


def update(request):
	interest_string = request.POST.get("interest_list")
	user = getUser(request)
	for interest in user.interests.all():
		interest.freq -= 1
	user.interests.clear()
	if len(interest_string) > 0:
		interests = interest_string.split(",");
		for interest in interests:
			intr = Interest.objects.filter(id=interest)
			intr[0].freq += 1
			user.interests.add(intr[0])

		user.save()
	return redirect('/chat/')

