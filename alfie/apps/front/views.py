from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	return HttpResponse('index view -> <a href="about">about</a> | <a href="order">order</a><br><a href="accounts/signup">signup</a> | <a href="accounts/signin">signin</a>')

def about(request):
	return HttpResponse('This is about view -> <a href="/">go home</a>')