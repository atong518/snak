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

def show(request):
	i_tree = GetInterestTree()

	return render(request, 'interests/show.html', {})
