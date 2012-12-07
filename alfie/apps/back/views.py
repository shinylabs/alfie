from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Sum
#bigups http://stackoverflow.com/questions/5757094/decimal-zero-padding
from util import moneyfmt

from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Order

def index(request):
	profiles = Profile.objects.all()
	inv_count = Order.objects.aggregate(Sum('choice__size')).values()[0]
	total_rev = moneyfmt(Order.objects.aggregate(Sum('choice__price')).values()[0], curr='$')
	return render_to_response('back/index.html', {'profiles': profiles, 'inv_count': inv_count, 'total_rev': total_rev}, context_instance=RequestContext(request))