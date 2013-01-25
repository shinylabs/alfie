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

# stripe tools
from alfie.apps.back.finance.stripeutil import *

def customer():
	pass

def inventory():
	pass

def financial():
	pass

def backoffice(request):
	profiles = Profile.objects.all()
	a_count = Profile.objects.filter(choice__id=1).count()
	b_count = Profile.objects.filter(choice__id=2).count()
	c_count = Profile.objects.filter(choice__id=3).count()

	inv_count = Order.objects.aggregate(Sum('choice__slots')).values()[0]
	box_a_count = Order.objects.filter(choice__id=1).filter(created__month=now.month).count()
	box_b_count = Order.objects.filter(choice__id=2).filter(created__month=now.month).count()
	box_c_count = Order.objects.filter(choice__id=3).filter(created__month=now.month).count()

	try:
		total_rev = moneyfmt(Order.objects.aggregate(Sum('choice__price')).values()[0], curr='$')
	except:
		total_rev = 0

	return render_to_response('back/office.html', {'profiles': profiles, 'a_count': a_count, 'b_count': b_count, 'c_count': c_count, 'inv_count': inv_count, 'box_a_count': box_a_count, 'box_b_count': box_b_count, 'box_c_count': box_c_count, 'total_rev': total_rev}, context_instance=RequestContext(request))


def finance_tools(request):
	return render_to_response('back/finance_tools.html', context_instance=RequestContext(request))

def finance_coupon(request):
	# When a form is sent
	if request.method == 'POST': 
		coupon_id = request.POST['id']
		percent_off = request.POST['percent_off']
		max_redemptions = request.POST['max']
		response = create_coupon(name=coupon_id, percent_off=percent_off, max_redemptions=max_redemptions)
		return HttpResponse(response)

	coupons = coupon_list()
	return render_to_response('back/finance_coupon.html', {'coupons': coupons}, context_instance=RequestContext(request))

def logistics_tools(request):
	return render_to_response('back/logistics_tools.html', context_instance=RequestContext(request))

# http://www.nerdydork.com/django-filter-model-on-date-range.html