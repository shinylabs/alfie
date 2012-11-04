from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	return HttpResponse('')

def about(request):
	return HttpResponse('This is about view -> <a href="/">go home</a>')