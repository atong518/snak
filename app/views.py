from django.shortcuts import render
from app.models import ProspieUser, CollegeUser
from app.forms import ProspieSignupForm, CollegeSignupForm
from django.shortcuts import render_to_response

# Create your views here.
def splash(request):
    return render(request, 'app/splash.html', {})

def sign_up(request):
    prospieform = ProspieSignupForm(instance=ProspieUser())
    collegeform = CollegeSignupForm(instance=CollegeUser())

    return render_to_response('app/sign_up.html', 
                              {'prospie_form': prospieform, 
                               'college_form': collegeform})
