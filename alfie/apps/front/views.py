from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	return HttpResponse('<html><head><title>LuckyRamenCat MVP</title></head><body><h1>LuckyRamenCat</h1><p><a href="about">about</a> | <a href="accounts/signup">signup</a> | <a href="accounts/signin">signin</a></p><h2><a href="order">Order now</a></h2></body></html>')

def about(request):
	return HttpResponse('This is about view -> <a href="/">go home</a>')