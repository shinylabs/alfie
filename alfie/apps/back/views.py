"""
//SHELL CMDS

from alfie.apps.orders.models import *
"""

#### time utilities ####
#todo - move these to a separate module or util file
import datetime
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
#bigups http://stackoverflow.com/questions/5757094/decimal-zero-padding
from util import moneyfmt

# data
from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Order, Menu
from alfie.apps.ramens.models import Brand, Flavor, Ramen, Box

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
	total_brand_count = Brand.objects.all().count()
	total_ramen_count = Ramen.objects.all().count()

	html = 	"<h1>Inventory</h1><p>Total brands: %s <br> %s from China <br> %s from USA<br><br>Total ramen: %s</p>" % (total_brand_count, china_count, usa_count, total_ramen_count)

	return HttpResponse(html)

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
	month_count = Order.objects.this_month().count()
	paid_count = Order.objects.this_month_paid().count()
	shipped_count = Order.objects.this_month_shipped().count()
	html = "<h1>Orders</h1><p>Total orders: %s<br>%s this month <br> %s paid this month <input type='button' value='charge orders'> <br> %s shipped this month <input type='button' value='ship orders'></p>" % (total_count, month_count, paid_count, shipped_count)

	return HttpResponse(html)

class OrderListView(ListView):
	pass

class OrderDetailView(DetailView):
	pass


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



"""

Profit/Loss

Revenue
(Products)
(Costs)
(Fees)
(Shipping)
===
Total

"""