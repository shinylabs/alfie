from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def signup(request):
	return HttpResponse('signup as new user -> <a href="/signup">signup</a>')

def login(request):
	return HttpResponse('login -> <a href="/login">login</a>')

def logout(request):
	return HttpResponse('logout-> <a href="/logout">logout</a>')

def payment(request):
	return render_to_response('stripes/payment.html', context_instance=RequestContext(request))


"""

LOGIN FLOW

index -> login -> view profile -> edit profile, cancel, upgrade, history

"""