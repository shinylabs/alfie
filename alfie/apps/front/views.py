from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
	if request.user.is_authenticated():
		#bigups http://stackoverflow.com/questions/2567801/display-user-name-in-reference-to-user-id-in-django-template
		return HttpResponseRedirect('/accounts/%s' % User.objects.get(id=request.user.id).username)
	else:
		return render_to_response('front/index.html', context_instance=RequestContext(request))