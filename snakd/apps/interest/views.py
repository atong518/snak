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


# list of mobile User Agents
mobile_uas = [
    'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
    'blaz','brew','cell','cldc','cmd-','dang','doco','eric','hipt','inno',
    'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
    'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
    'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
    'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
    'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
    'tosh','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
    'wapr','webc','winw','winw','xda','xda-'
    ]
 
mobile_ua_hints = [ 'SymbianOS', 'Opera Mini', 'iPhone', 'Android' ]

def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''
 
    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]
 
    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True

    return mobile_browser

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

	if not mobileBrowser(request):
		template = 'interests/show.html'
	else:
		template = 'interests/show_mobile.html'

	return render(request, template, responsedict)


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

