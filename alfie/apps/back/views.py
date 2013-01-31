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

# data
from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Order, Menu
from alfie.apps.ramens.models import Brand, Flavor, Ramen

# stripe tools
from alfie.apps.back.finance.stripeutil import *

def backoffice(request):
	return HttpResponse('<a href="inventory">Inventory</a> | <a href="orders">Orders</a> | <a href="finances">Finances</a> | <a href="shipping">Shipping</a> | <a href="customers">Customers</a> ')

def inventory_index(request):
	"""
		Manages ramens, brands, boxes
	"""
	china_count = Brand.objects.country_count('China')
	usa_count = Brand.objects.country_count('USA')
	total_count = Brand.objects.all().count()
	return HttpResponse('Total brands: %s <br> %s from China <br> %s from USA' % (total_count, china_count, usa_count))

def orders_index(request):
	"""
		Manages orders current and past

		Get total orders
		Get orders for this month
		Get orders for last month
		Get orders for the past three months

		Get paid orders 
		Get orders to be paid

		Get orders to be shipped
		Get shipped orders

		Menu tools:
			- CRUD menu
			- breakdown menu
	"""
	return HttpResponse('orders this month: %s' % Order.objects.monthly_total())

def finances_index(request):
	"""
		Manages finances processes, produces reports, interfaces with Stripe

		Show payment queue

		Show finance tools
			- CRUD coupons
			- poke deadbeats
	"""
	return HttpResponse('orders paid up this month: %s' % Order.objects.monthly_paid_total())

def shipping_index(request):
	"""
		Manages shipping processes

		Show ship queue

		Show shipping tools

		TODO:
			Users without admin permissions can only see/interact with this view

	"""
	return HttpResponse('orders shipped this month: %s' % Order.objects.monthly_shipped_total())

def customers_index(request):
	"""
		Manages customers processes and services

		Segment to lists:
			- good customers
			- bad customers

		Show service tools
	"""
	return HttpResponse('customers')




def backoffice_old(request):
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

	return render_to_response('back/office.html', {'a_count': a_count, 'b_count': b_count, 'c_count': c_count, 'inv_count': inv_count, 'box_a_count': box_a_count, 'box_b_count': box_b_count, 'box_c_count': box_c_count, 'total_rev': total_rev}, context_instance=RequestContext(request))

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