from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponseRedirect

def home(request):
    return HttpResponseRedirect('/blog')