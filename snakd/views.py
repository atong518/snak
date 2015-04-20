from django.shortcuts import render_to_response, render
from django.template import RequestContext

def errorhandler(request):

    return render(request, 'user/fourohfour.html', {})
