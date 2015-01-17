from django.shortcuts import render
from app.models import ProspieUser, CollegeUser
from app.forms import ProspieSignupForm, CollegeSignupForm
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def splash(request):
    return render(request, 'app/splash.html', {})

def sign_up(request):

    return render(request, 'app/sign_up.html', {})

def howto(request):
    return render(request, 'app/howto.html', {})

def aboutus(request):
    return render(request, 'app/aboutus.html', {})

    if request.method == "POST":
        prospieform = ProspieSignupForm(request.POST)
        collegeform = CollegeSignupForm(request.POST)

        if prospieform.is_valid():
            new_student = prospieform.save(commit=False)
            new_student.save()
            return render(request,
                          "app/main.html",
                          {})

        if collegeform.is_valid():
            new_student = collegeform.save(commit=False)
            new_student.save()
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

def login(request):
    email = password = ''
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request,
                          'app/main.html',
                          {})

    return render(request,
                  'app/login.html',
                  {'email': email})

def main(request):
    return render(request,
                  "app/main.html",
                  {})

