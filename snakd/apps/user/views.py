from django.shortcuts import render, HttpResponseRedirect
from snakd.apps.user.models import ProspieUser, CollegeUser, GenericUser
from snakd.apps.user.forms import ProspieSignupForm, CollegeSignupForm, GenericSignupForm
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import update_session_auth_hash
from snakd.lib.match import bestmatch
from snakd.lib.matrix import getMatrix
# Create your views here.
def splash(request):
    if request.user.is_authenticated():
        return redirect("snakd.apps.chat.views.chat")

    return render(request, 'user/splash.html', {})

def _specify_class(user):
    try:
        user = user.collegeuser
    except:
        user = user.prospieuser
    return user

def _send_mail(email, activation_code):
    # Email shenanigans
    subject = "SnakDartmouth Email Verification"
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
            return redirect("/chat/")

        if request.POST.get("college_signup") is not None and collegeform.is_valid():
            new_student = collegeform.save_user(collegeform.cleaned_data)
            _send_mail(new_student.email, new_student.activation_code)
            user = authenticate(email=new_student.email, password=collegeform.cleaned_data["password1"])
            auth_login(request, user)
            return redirect("/chat/")

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

def main(request):
    return render(request, "user/main.html", {})

def login(request):
    email = password = ''
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/chat/")

    return render(request,
                  'user/login.html',
                  {'email': email})

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
            params = request.POST.dict()
            if user.check_password(params.pop('password')):
                user.updateUser(**params)
                update_session_auth_hash(request, user)
                dic = user.editableFields()
            else:
                # TODO?: What should happen here?
                dic = user.editableFields()
        elif request.method == "GET":
            dic = user.editableFields()
        else:  # TODO: Will need a delete method here
            import pdb; pdb.set_trace()

        return render(request, 'user/settings.html', dic)
    except:
        return HttpResponseRedirect('/')



def match(request):
    try:
        uid = request.session.get("_auth_user_id")
        user = GenericUser.objects.get(id=uid)
        user = _specify_class(user)
        if isinstance(user, CollegeUser):
            opplist = ProspieUser.objects.all()
        else:
            opplist = CollegeUser.objects.all()
        matrix = getMatrix()
        best = bestmatch(matrix, user, opplist)
        user.matches.add(best)
        return HttpResponseRedirect('/chat/')
    except:
        return HttpResponseRedirect('/')



























