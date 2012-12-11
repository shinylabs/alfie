# time
import datetime
now = datetime.datetime.now()
# <3 months
#three_months_ago = now - timedelta(months=3)

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Sum
#bigups http://stackoverflow.com/questions/5757094/decimal-zero-padding
from util import moneyfmt

from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Order

def customer():
	pass

def inventory():
	pass

def financial():
	pass

def backoffice(request):
	profiles = Profile.objects.all()

	inv_count = Order.objects.aggregate(Sum('choice__size')).values()[0]
	box_a_count = Order.objects.filter(choice__id=1).filter(created__month=now.month).count()
	box_b_count = Order.objects.filter(choice__id=2).filter(created__month=now.month).count()
	box_c_count = Order.objects.filter(choice__id=3).filter(created__month=now.month).count()

	total_rev = moneyfmt(Order.objects.aggregate(Sum('choice__price')).values()[0], curr='$')
	return render_to_response('back/office.html', {'profiles': profiles, 'inv_count': inv_count, 'box_a_count': box_a_count, 'box_b_count': box_b_count, 'box_c_count': box_c_count, 'total_rev': total_rev}, context_instance=RequestContext(request))


def finance_tools(request):
	return render_to_response('back/finance_tools.html', context_instance=RequestContext(request))

def logistics_tools(request):
	return render_to_response('back/logistics_tools.html', context_instance=RequestContext(request))

# http://www.nerdydork.com/django-filter-model-on-date-range.html