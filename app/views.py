from django.shortcuts import render
from app.models import ProspieUser, CollegeUser
from app.forms import ProspieSignupForm, CollegeSignupForm
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives


# Create your views here.
def splash(request):
    return render(request, 'app/splash.html', {})

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


        if prospieform.is_valid():
            new_student = prospieform.save_user(prospieform.cleaned_data)
            _send_mail(new_student.email, new_student.activation_code)
            # log in the new user and redirect to main page
            user = authenticate(email=new_student.email, password=prospieform.cleaned_data["password1"])
            auth_login(request, user)
            return render(request,
                          "app/main.html",
                          {})

        if collegeform.is_valid():
            new_student = collegeform.save_user(collegeform.cleaned_data)
            _send_mail(new_student.email, new_student.activation_code)
            user = authenticate(email=new_student.email, password=collegeform.cleaned_data["password1"])
            auth_login(request, user)
            return render(request,
                          "app/main.html",
                          {})

    else:
        prospieform = ProspieSignupForm()
        collegeform = CollegeSignupForm()

    return render(request, 
                  'app/sign_up.html', 
                  {'prospie_form': prospieform, 
                   'college_form': collegeform})

def howto(request):
    return render(request, 'app/howto.html', {})

def aboutus(request):
    return render(request, 'app/aboutus.html', {})

def main(request):
    return render(request,
                  "app/main.html",
                  {})

def login(request):
    email = password = ''
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(main)

    return render(request,
                  'app/login.html',
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

<<<<<<< HEAD
def interests(request):
    return render(request,
                  "app/interests.html",
                  {})

=======
    return redirect(main)
    
>>>>>>> cfde78248e9b1ae2394f170d2887c8e0f4e158f2
