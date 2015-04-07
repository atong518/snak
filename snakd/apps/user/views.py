from django.shortcuts import render, HttpResponseRedirect
from snakd.apps.user.models import ProspieUser, CollegeUser, GenericUser
from snakd.apps.user.forms import ProspieSignupForm, CollegeSignupForm, CollegeSettingsForm, ProspieSettingsForm
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import update_session_auth_hash
from snakd.lib.match import bestmatches
from snakd.lib.matrix import getMatrix
from datetime import datetime, timedelta
import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from snakd.apps.user.forms import ContactUsForm
from django.template import RequestContext, Context
#from django import newforms as forms
from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError


# Create your views here.
def splash(request):
    if request.user.is_authenticated():
        return redirect("/chat/")

    return render(request, 'user/splash.html', {})

def _specify_class(user):
    try:
        user = user.collegeuser
    except:
        user = user.prospieuser
    return user

def _send_mail(email, activation_code):
    # Email shenanigans
    subject = "Sagely Email Verification"
    message = "Welcome to SnakDartmouth, we very much appreciate your signing up!\n"
    from_email = settings.EMAIL_HOST_USER

    url = "http://0.0.0.0:5000/confirm_email/" + activation_code + "/" + email + "/"
    txt_message = message + "Click here to activate your account: " + url
    html_message = message + "\nClick "
    html_message += "<a href=\"" + url + "\">"
    html_message += "here</a> to activate your account :)"
    msg = EmailMultiAlternatives(subject, txt_message, from_email, {email})
    msg.attach_alternative(html_message, "text/html")
    msg.send()

def sign_up(request):
    if request.method == "POST":
        prospieform = ProspieSignupForm(request.POST)
        collegeform = CollegeSignupForm(request.POST)


        if  request.POST.get("prospie_signup") is not None and prospieform.is_valid():
            new_student = prospieform.save_user(prospieform.cleaned_data)
            _send_mail(new_student.email, new_student.activation_code)
            # log in the new user and redirect to chat page
            user = authenticate(email=new_student.email, password=prospieform.cleaned_data["password1"])
            auth_login(request, user)
            return redirect("/interest/show/")

        if request.POST.get("college_signup") is not None and collegeform.is_valid():
            new_student = collegeform.save_user(collegeform.cleaned_data)
            _send_mail(new_student.email, new_student.activation_code)
            user = authenticate(email=new_student.email, password=collegeform.cleaned_data["password1"])
            auth_login(request, user)
            return redirect("/interest/show/")

    else:
        prospieform = ProspieSignupForm()
        collegeform = CollegeSignupForm()

    return render(request, 
                  'user/sign_up.html', 
                  {'prospie_form': prospieform, 
                   'college_form': collegeform})

def howto(request):
    return render(request, 'user/howto.html', {})

def aboutus(request):
    return render(request, 'user/aboutus.html', {})

def contactus(request):
    if request.method == "POST":
        contactform = ContactUsForm(request.POST)
        if  request.POST.get("contactus_button") is not None and contactform.is_valid():
            # Email shenanigans                                                                                                   
            subject = "Sagely.io Contact Us Comment"
            message = contactform.cleaned_data['contact_comments']
            email = settings.EMAIL_HOST_USER
            msg = EmailMultiAlternatives(subject, message, email, {email})
            msg.send()
            return redirect("/thankyou/")
    else: 
        contactform = ContactUsForm()
    return render(request, 'user/contactus.html', {'contactus_form': contactform})

def thankyou(request):
    return render(request, 'user/thankyou.html', {})

def main(request):
    return render(request, "user/main.html", {})

def login(request):
    email = password = ''
    has_error = "none"
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/chat/")
        else:
            has_error = "block"

    return render(request,
                  'user/login.html',
                  {'email': email,
                   'has_error': has_error})

def change_password(request):
    error = ""
    if request.POST:
        password = request.POST.get('old-password')
        user = authenticate(email=request.user.email, password=password)
        if user is not None:
            user.set_password(request.POST.get('new-password-1'))
            user.save()
            return redirect("/login/")
        else:
            error = "FALSE.  That is not your current password."
    return render(request,
                  'user/change_password.html',
                  {'error': error})

def confirm_email(request, activation_code, email):
    try:
        user = ProspieUser.objects.get(email=email)
    except ProspieUser.DoesNotExist:
        user = None

    if user is None:
        try: 
            user = CollegeUser.objects.get(email=email)
        except CollegeUser.DoesNotExist:
            user = None

    if user is not None and user.activation_code == activation_code:
        user.is_active = True
        user.save()
    
    return redirect("/chat/")

def edit(request):
    try:
        uid = request.session.get("_auth_user_id")
        user = GenericUser.objects.get(id=uid)
        user = _specify_class(user)
        if request.method == "POST":
            if isinstance(user, CollegeUser):
                form = CollegeSettingsForm(request.POST, instance=user)
            else:
                form = ProspieSettingsForm(request.POST, instance=user)
            # Update fields if password is correct
            if user.check_password(request.POST['password']):
                user = form.update_user(request.POST)
                # Update session
                update_session_auth_hash(request, user)
            else:
                # TODO?: What should happen here?
                pass
        if isinstance(user, CollegeUser):
            form = CollegeSettingsForm(instance=user)
        else:
            form = ProspieSettingsForm(instance=user)
        return render(request, 'user/settings.html', {'settings_form': form})
    except:
        return redirect('/')

def match(request):
    try:
        uid = request.session.get("_auth_user_id")
        user = GenericUser.objects.get(id=uid)
        user = _specify_class(user)
        try:
            if isinstance(user, CollegeUser):
                opplist = ProspieUser.objects.filter().exclude(
                    matches__id__contains=user.id)
            else:
                opplist = CollegeUser.objects.filter(
                    next_match__lte=datetime.now()).exclude(
                    matches__id__contains=user.id)
            matrix = getMatrix()
            possibleusers = bestmatches(matrix, user, opplist)
            # TODO: Gross hack caused by async request:
            # Django can't template the model since we determine
            # the match at a different time. This will work but
            # it's definitely not ideal...
            possibles = []
            for usr in possibleusers:
                possibles.append(usr.matchInfo())
        except:
            possibles = []
        return HttpResponse(
            json.dumps({"possibles": possibles}), 
            content_type='application/json')
    except:
        return HttpResponseRedirect('/')

