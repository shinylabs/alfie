"""
// REMEMBER, REMEMBER

FAT MODELS, SKINNY CONTROLLERS

"""


"""
// SHELL CMDS

from alfie.apps.orders.models import *
"""

#### time utilities ####
#todo - move these to a separate module or util file
import datetime
import calendar
now = datetime.datetime.now()

#bigups http://blog.e-shell.org/94
months_choices = []
for i in range(1,13): months_choices.append((i, datetime.date(now.year, i, 1).strftime('%B')))

#bigups http://stackoverflow.com/questions/4130922/how-to-increment-datetime-month-in-python
def add_months(sourcedate, months):
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month / 12
	month = month % 12 + 1
	day = min(sourcedate.day, calendar.monthrange(year,month)[1])
	return datetime.date(year, month, day)

def subtract_months(sourcedate, months):
	month = sourcedate.month - 1 - months
	year = sourcedate.year + month / 12
	month = month % 12 + 1
	day = min(sourcedate.day, calendar.monthrange(year,month)[1])
	return datetime.date(year, month, day)
#########################

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models import Count
#bigups http://stackoverflow.com/questions/5757094/decimal-zero-padding
from util import moneyfmt

# data
from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Order, Menu
from alfie.apps.ramens.models import Brand, Flavor, Ramen, Box

# stripe tools
from alfie.apps.back.finance.stripeutil import *

def backoffice(request):
	return render_to_response('back/_index.html', context_instance=RequestContext(request))

def inventory_index(request):
	"""
		Manages ramens, brands, boxes
	"""
	brand_origins = Brand.objects.values('origin').annotate(num_of_ramens=Count('id')).order_by('-num_of_ramens')
	ramen_origins = Ramen.objects.values('brand__origin').annotate(num_of_ramens=Count('id')).order_by('-num_of_ramens')
	total_brand_count = Brand.objects.all().count()
	total_ramen_count = Ramen.objects.all().count()

	return render_to_response('back/inventory_index.html', 
		{
		 'brand_origins': brand_origins, 
		 'ramen_origins': ramen_origins, 
		 'total_brand_count': total_brand_count, 
		 'total_ramen_count': total_ramen_count
		 }, 
		context_instance=RequestContext(request))

def orders_index(request):
	"""
		Manages orders current and past

		Get total count: 
			total_count = Order.objects.count()
		Get count for this month:
			month_count = Order.objects.this_month().count()
		Get count for last month:
			last_month_count = Order.objects.prev_month().count()
		Get count for the past three months:
			last_quarter_count = Order.objects.quarterly().count()
		Get count for any month:
			new_month_count = Order.objects.this_month(datetime_object).count()

		Get paid orders count:
			paid_count = Order.objects.this_month_paid()
		Get unpaid orders:
			unpaid_list = Order.objects.unpaid_list()

		Get shipped orders count:
			shipped_count = Order.objects.this_month_shipped()
		Get unshipped orders:
			unshipped_list = Order.objects.unshipped_list()

		Menu tools:
			- CRUD menu
			- breakdown menu
	"""
	total_count = Order.objects.count()
	prev_month_count = Order.objects.prev_month().count()
	this_month_count = Order.objects.this_month().count()
	next_month_count = Order.objects.this_month(add_months(now, 1)).count()

	prev_paid_count = Order.objects.prev_month_paid().count()
	paid_count = Order.objects.this_month_paid().count()
	next_paid_count = Order.objects.this_month_paid(add_months(now, 1)).count()

	prev_shipped_count = Order.objects.prev_month_shipped().count()
	shipped_count = Order.objects.this_month_shipped().count()
	next_shipped_count = Order.objects.this_month_shipped(add_months(now, 1)).count()

	return render_to_response('back/orders_index.html', 
		{	
		 'total_count': total_count, 
		 'prev_month_count': prev_month_count, 
		 'this_month_count': this_month_count, 
		 'next_month_count': next_month_count,
		 'prev_paid_count': prev_paid_count,
		 'paid_count': paid_count, 
		 'next_paid_count': next_paid_count,
		 'prev_shipped_count': prev_shipped_count,
		 'shipped_count': shipped_count,
		 'next_shipped_count': next_shipped_count
		 }, 
		context_instance=RequestContext(request))

def finances_index(request):
	"""
		Manages finances processes, produces reports, interfaces with Stripe

		Show payment queue

		Show finance tools
			- CRUD coupons
			- poke deadbeats
	"""
	from decimal import *
	total_count = Order.objects.count()
	this_month_count = Order.objects.this_month().count()
	unpaid_list = Order.objects.unpaid_list()
	revenue = Decimal(Order.objects.this_month().aggregate(Sum('choice__price'))['choice__price__sum']) / 100
	shipping_costs = Decimal(Order.objects.this_month().aggregate(Sum('shipping_cost'))['shipping_cost__sum']) / 100
	product_costs = Decimal(Order.objects.this_month().aggregate(Sum('product_cost'))['product_cost__sum']) / 100
	fees = Decimal(Order.objects.this_month().aggregate(Sum('stripe_fee'))['stripe_fee__sum']) / 100
	profit = revenue - shipping_costs - product_costs - fees

	return render_to_response('back/finances_index.html', 
		{	
		 'total_count': total_count, 
		 'this_month_count': this_month_count,
		 'unpaid_list': unpaid_list,
		 'revenue': revenue,
		 'shipping_costs': shipping_costs,
		 'product_costs': product_costs,
		 'fees': fees,
		 'profit': profit
		 }, 
		context_instance=RequestContext(request))


def shipping_index(request):
	"""
		Manages shipping processes

		Show ship queue

		Show shipping tools

		TODO:
			Users without admin permissions can only see/interact with this view

	"""
	total_count = Order.objects.count()
	unshipped_list = Order.objects.unshipped_list()

	return render_to_response('back/shipping_index.html', 
		{	
		 'total_count': total_count, 
		 'unshipped_list': unshipped_list
		 }, 
		context_instance=RequestContext(request))

def customers_index(request):
	"""
		Manages customers processes and services

		Segment to lists:
			- good customers
			- bad customers

		Show service tools
	"""
	total_count = Profile.objects.count()
	return render_to_response('back/customers_index.html', 
		{	
		 'total_count': total_count
		 }, 
		context_instance=RequestContext(request))

# http://www.nerdydork.com/django-filter-model-on-date-range.html



"""

#todo

1. Templates
2. Actions
3. Reporting

Profit/Loss Report
	Revenue
	(Products)
	(Costs)
	(Fees)
	(Shipping)
	===
	Total

"""