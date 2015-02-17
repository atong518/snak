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


def show(request):
	responsedict = {}
	responsedict["i_list"] = GetInterestTree()
	# Test user interest until we have actual population data
	# responsedict["user_interests"] = json.dumps([{
	# 	"name": 5,
	# 	"id": 44,
	# 	"tooltip": "testing 1 2 3",
	# 	"weight": 1,
	# }])
	# import pdb; pdb.set_trace()
	responsedict["user_interests"] = json.dumps([])
	return render(request, 'interests/show.html', responsedict)
