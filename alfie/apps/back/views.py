from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
	return render_to_response('back/index.html', context_instance=RequestContext(request))