from django.shortcuts import render
from app.models import ProspieUser, CollegeUser
from app.forms import ProspieSignupForm, CollegeSignupForm
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def splash(request):
    return render(request, 'app/splash.html', {})

def sign_up(request):
    if request.method == "POST":
        prospieform = ProspieSignupForm(request.POST)
        collegeform = CollegeSignupForm(request.POST)

        if prospieform.is_valid():
            new_student = prospieform.save(commit=False)
            new_student.save()

        if collegeform.is_valid():
            new_student = collegeform.save(commit=False)
            new_student.save()
    else:
        prospieform = ProspieSignupForm()
        collegeform = CollegeSignupForm()

    return render(request, 
                  'app/sign_up.html', 
                  {'prospie_form': prospieform, 
                   'college_form': collegeform})
