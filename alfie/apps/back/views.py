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
from django.core.context_processors import csrf
from django.db.models import Sum, Avg, Max, Count
#bigups http://stackoverflow.com/questions/5757094/decimal-zero-padding
from util import moneyfmt

# data
from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Order, Menu
from alfie.apps.ramens.models import Brand, Flavor, Ramen, Box
from alfie.apps.services.models import Service

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

	return render_to_response('back/inventory_index.html', {
			'brand_origins': brand_origins, 
			'ramen_origins': ramen_origins, 
			'total_brand_count': total_brand_count, 
			'total_ramen_count': total_ramen_count
		}, context_instance=RequestContext(request))

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

	return render_to_response('back/orders_index.html', {	
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
		}, context_instance=RequestContext(request))

def finances_index(request):
	"""
		Manages finances processes, produces reports, interfaces with Stripe

		Show payment queue

		Show finance tools
			- CRUD coupons
			- poke deadbeats
	"""
	this_month = Order.objects.this_month()
	this_months_book = dict()

	# Revenue
	this_months_book['revenue'] = float((this_month.aggregate(Sum('choice__price'))['choice__price__sum'])) / 100

	# Costs
	total_cost = 0
	for cost in [field.name for field in Order._meta.fields if field.name.endswith('cost') or field.name.endswith('fee')]:
		this_months_book[cost] = float((this_month.aggregate(Sum(cost))[cost+'__sum'])) / 100
		total_cost += this_months_book[cost]

	# Profit
	this_months_book['profit'] = this_months_book['revenue'] - total_cost

	# This month
	this_months_book['this_month_count'] = this_month.count()

	# Total
	this_months_book['total_count'] = Order.objects.count()

 	if request.method == 'POST': # If the form has been submitted...
		amt = int(request.POST['amt']) * 100
		item = request.POST['lineitem']
		Order.objects.add_lineitem(amt, item, this_month)
		return HttpResponseRedirect('')

	#tasks debug http://stackoverflow.com/questions/3553955/refresh-template-in-django

	unpaid = Order.objects.this_month_unpaid()

	return render_to_response('back/finances_index.html', {	
			'this_months_book': this_months_book,
			'unpaid': unpaid
		}, context_instance=RequestContext(request))


def shipping_index(request):
	"""
		Manages shipping processes

		Show ship queue

		Show shipping tools

		TODO:
			Users without admin permissions can only see/interact with this view

	"""

	boxes_this_month = Box.objects.this_month()

 	if request.method == 'POST': 	# If the form has been submitted...
 		amt = int(request.POST['amt'])

 		if '1' in request.POST:
 			if boxes_this_month[0].orders.this_month_to_pack().count() > 0:
 				for order in boxes_this_month[0].orders.this_month_to_pack()[0:amt]:
 					order.got_packed()
 					order.save()
		if '2' in request.POST:
 			if boxes_this_month[1].orders.this_month_to_pack().count() > 0:
 				for order in boxes_this_month[1].orders.this_month_to_pack()[0:amt]:
 					order.got_packed()
 					order.save()
		if '3' in request.POST:
 			if boxes_this_month[2].orders.this_month_to_pack().count() > 0:
 				for order in boxes_this_month[2].orders.this_month_to_pack()[0:amt]:
 					order.got_packed()
 					order.save()
		return HttpResponseRedirect('')

	manifest_this_month = Order.objects.this_month_manifest()

	total_sum = 0
	total_avg = 0
	states = Profile.objects.values('ship_state').annotate(customers=Count('id')).order_by('-customers')
	for i in states:
	  state = i['ship_state']
	  customers = i['customers']
	  #bigups http://agiliq.com/blog/2009/08/django-aggregation-tutorial/
	  state_avg = float(Profile.objects.filter(ship_state=state).aggregate(Avg('shipping_rate'))['shipping_rate__avg']) / 100
	  state_sum = float(Profile.objects.filter(ship_state=state).aggregate(Sum('shipping_rate'))['shipping_rate__sum']) / 100
	  state_max = float(Profile.objects.filter(ship_state=state).aggregate(Max('shipping_rate'))['shipping_rate__max']) / 100
	  #print "State: %s - Customers: %s - Average: $%.2f - Max: $%.2f - Total: $%.2f" % (state, customers, state_avg, state_max, state_sum)
	  total_sum += state_sum
	  total_avg += state_avg
	  i['avg'] = round(state_avg, 2)
	  i['sum'] = round(state_sum, 2)
	  i['max'] = round(state_max, 2)
	#print "Total sum: $%.2f - Total avg: $%.2f" % (total_sum, (total_avg / len(states)))

	return render_to_response('back/shipping_index.html', {	
			'states': states,
			'total_sum': total_sum,
			'total_avg': (total_avg / len(states)),
			'boxes_this_month': boxes_this_month,
			'manifest_this_month': manifest_this_month
		}, context_instance=RequestContext(request))

def customers_index(request):
	"""
		Manages customers processes and services

		Segment to lists:
			- good customers
			- bad customers

		Show service tools
	"""
	profits = []
	total_profit = 0 
	for i in range(Profile.objects.count()):
	  customer = Profile.objects.all()[i]
	  order = customer.user.orders.all()[0]
	  profit = order.choice.price - order.check_costs()
	  box_name = order.choice.name.title()
	  #print "%s shipped to %s profit: $%.2f" % (box_name, customer.ship_state, (float(profit)/100))
	  total_profit += profit

	  dict = {}
	  dict['user'] = customer.user.id
	  dict['name'] = customer.user.first_name + ' ' + customer.user.last_name
	  dict['state'] = customer.ship_state
	  dict['box'] = box_name
	  dict['revenue'] = "$%.2f" % (float(order.choice.price) / 100)
	  dict['costs'] = "$%.2f" % (float(order.check_costs()) / 100)
	  dict['profit'] = "$%.2f" % (float(profit) / 100)
	  profits.append(dict)
	#print "$%.2f" % (float(total_profit)/100)

	#bigups http://stackoverflow.com/questions/72899/in-python-how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary
	#profits_by_profit = sorted(profits, key=lambda k: k['profit'])
	profits_by_state = sorted(profits, key=lambda k: k['state'])

	return render_to_response('back/customers_index.html', {
			'profits_by_state': profits_by_state
		}, context_instance=RequestContext(request))

# http://www.nerdydork.com/django-filter-model-on-date-range.html

def services_index(request):
	service_orders = Service.objects.all()
	return render_to_response('back/services_index.html', {
			'service_orders': service_orders
		}, context_instance=RequestContext(request))



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