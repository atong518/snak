from django.shortcuts import render, HttpResponseRedirect, render_to_response, redirect
from snakd.apps.user.models import ProspieUser, CollegeUser, GenericUser
from snakd.apps.user.forms import ProspieSignupForm, CollegeSignupForm, CollegeSettingsForm, ProspieSettingsForm
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import update_session_auth_hash
from snakd.lib.match import bestmatches, randommatches
from snakd.lib.matrix import getMatrix
from datetime import datetime, timedelta
import json
import re
from snakd.apps.user.forms import ContactUsForm
#from django import newforms as forms
from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError
from snakd.apps.chat.models import Thread


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
    message = "Welcome to Sagely, thank you for signing up!!\n"
    from_email = "sagelyio@gmail.com"

    url = "http://www.sagely.io/confirm_email/" + activation_code + "/" + email + "/"
    txt_message = message + "Click here to activate your account: " + url
    html_message = message + "\nClick "
    html_message += "<a href=\"" + url + "\">"
    html_message += "here</a> to activate your account :)"
    msg = EmailMultiAlternatives(subject, txt_message, from_email, {email})
    msg.attach_alternative(html_message, "text/html")
    msg.send()

def resend_confirmation_email(request):
    uid = request.session.get("_auth_user_id")
    user = GenericUser.objects.get(id=uid)

    _send_mail(user.email, user.activation_code)

    return redirect("/chat/")

def sign_up(request):
    if request.method == "POST":
        existing_user = GenericUser.objects.filter(email__iexact=request.POST.get('email'))
        if existing_user:
            confirmation_text = "Oops! We already have an account with that email. Maybe try logging in?"
            messages.add_message(request, messages.INFO, confirmation_text, fail_silently=True)
            redirect('sign_up')

        prospieform = ProspieSignupForm(request.POST)
        collegeform = CollegeSignupForm(request.POST)
        studenttype = request.POST.get("type", "prospie")

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
        studenttype = "prospie"

    if not mobileBrowser(request):
        template = 'user/sign_up.html'
    else:
        template = 'user/sign_up_mobile.html'

    return render(request, 
                  template,
                  {'prospie_form': prospieform, 
                   'college_form': collegeform,
                   'student_type': studenttype})

def howto(request):
    return render(request, 'user/howto.html', {})

def aboutus(request):
    return render(request, 'user/aboutus.html', {})

def howmatchingworks(request):
    return render(request, 'user/howmatchingworks.html', {})

def validateE(email):
    if len(email) > 6:
        if re.match('\w[\w\.-]*@\w[\w\.-]+\.\w+', email) != None:
            return 1
    return 0

def contactus(request):
    if request.method == "POST":
        contactform = ContactUsForm(request.POST)
        validateE(contactform.cleaned_data['user_email'])
        if  request.POST.get("contactus_button") is not None and contactform.is_valid():
            # Email shenanigans                                                                                                   
            subject = "Sagely.io Contact Us Comment from " + contactform.cleaned_data['user_email']
            message = contactform.cleaned_data['contact_comments']
#            txt_message = message + contactform.cleaned_data['user_email']
            email = "sagelyio@gmail.com"
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
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/chat/")
        else:
            confirmation_text = "Oops! We had some trouble logging you in. Try again?"
            messages.add_message(request, messages.INFO, confirmation_text, fail_silently=True)
            return redirect("login")

    return render(request,
                  'user/login.html',
                  {'email': email,
                   'has_error': has_error})


def send_password_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = "Sagely Password Reset"
        from_email = "sagelyio@gmail.com"
        html_message = "Reset your password <a href='http://www.sagely.io/reset_password/?email=" + email + "'>here</a>.<br><br>The Sagely Team"
        msg = EmailMultiAlternatives(subject, html_message, from_email, {email})
        msg.attach_alternative(html_message, "text/html")
        msg.send()

        return redirect("/chat/")
    else:
        return render(request,
            'user/email_reset.html')

def reset_password(request):
    if request.method == "POST":
        user = GenericUser.objects.filter(id=request.POST.get("user_id"))[0]
        user.set_password(request.POST.get("new-password-1"))
        user.save()
        return redirect("/chat/")
    else:
        email = request.GET.get('email', '')
        user = GenericUser.objects.filter(email__iexact=email)[0]
        user = _specify_class(user)
        return render(request,
              'user/reset_password.html',
              {'user_id': user.id})

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
    
    return render(request, 'user/password_confirmation.html', {})

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
                    matches__id__contains=user.id).exclude(
                    is_active=False)
            else:
                opplist = CollegeUser.objects.filter(
                    next_match__lte=datetime.now()).exclude(
                    matches__id__contains=user.id).exclude(
                    is_active=False)
                if (not user.is_active) and len(user.matches.all()) > 0:
                    return HttpResponse(
                        json.dumps({"possibles": [],
                                    "allow_matches": False}), 
                        content_type='application/json')
                elif not user.match_eligible():
                    return HttpResponse(
                        json.dumps({"possibles": [],
                                    "allow_matches": "ineligible"}), 
                        content_type='application/json')

            if request.POST.get("match-type") == "random":
                possibleusers = randommatches(user, opplist)
            else:
                matrix = getMatrix()
                possibleusers = bestmatches(matrix, user, opplist)

            possibles = []
            for usr in possibleusers:
                possibles.append(usr.matchInfo())
        except:
            possibles = []
        return HttpResponse(
            json.dumps({"possibles": possibles,
                        "allow_matches": True}), 
            content_type='application/json')
    except:
        return HttpResponseRedirect('/')

def about_match(request):
    thread = Thread.objects.filter(id=request.GET['thread_id'])[0]
    match = thread.members.exclude(email=request.user.email)[0]
    match = _specify_class(match)
    about = match.introText()
    return HttpResponse(
            json.dumps({"about": about}), 
            content_type='application/json')


