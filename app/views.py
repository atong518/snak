from django.shortcuts import render

# Create your views here.
def splash(request):
    return render(request, 'app/splash.html', {})

def sign_up(request):
    return render(request, 'app/sign_up.html', {})

def howto(request):
    return render(request, 'app/howto.html', {})

def aboutus(request):
    return render(request, 'app/aboutus.html', {})
