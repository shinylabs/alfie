# python
import datetime
now = datetime.datetime.now()

# django
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

# data
from django.contrib.auth.models import User
from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Menu, Order

# forms
from alfie.apps.orders.forms import MenuForm, UserForm, OrderForm
from alfie.apps.profiles.forms import SignupFormExtra


def startOrder(request):
	"""
		Shows off menu choices
	
		Input: selection
		Output: modelform

		1. Show menu pulled from modelform
		2. If no choice then reshow form
		3. If choice then process
	"""
	# When a form is sent
	if request.method == 'POST': 
		# Bound form to POST data
		form = MenuForm(request.POST)
		# What is the choice from form
		menu = form.data['menu']
		# Set session variable
		request.session['menu'] = menu
		return HttpResponseRedirect('/accounts/signup')
	
	# Initialize forms
	else:
		if 'menu' in request.session:
			if 'user' in request.session:
				return HttpResponseRedirect('/order/pay')
			else:
				menu = request.session['menu']
				return HttpResponseRedirect('/accounts/signup')
		else:
			# Some unbound forms
			orderform = OrderForm()
			menuform = MenuForm()
			userform = UserForm()
			return render_to_response('orders/order_form.html', {'orderform': orderform, 'menuform': menuform, 'userform': userform}, context_instance=RequestContext(request))		

def cancelOrder(request):
	# Reset variable in session
	if 'menu' in request.session:
		del request.session['menu']
	if 'user' in request.session:
		del request.session['user']
	# Redirect back to function
	return HttpResponseRedirect('/order/')

def payOrder(request):
	if request.method == 'POST':
		last_4_digits = '4242'
		request.session['last_4_digits'] = last_4_digits
		stripe_token = '12jiojio1jiojoi'
		request.session['stripe_token'] = stripe_token
		#bigups http://stackoverflow.com/questions/13328810/django-redirect-to-view
		return redirect('alfie.apps.orders.views.saveOrder')
	else:
		if 'menu' not in request.session or 'user' not in request.session:
			return HttpResponseRedirect('/order/')
		else:
			menu = request.session['menu']
			user = request.session['user']
			price = Menu.objects.get(pk=menu).price
			return render_to_response('orders/payment.html', {'menu': menu, 'price': price, 'user': user}, context_instance=RequestContext(request))

def saveOrder(request):
	if 'menu' in request.session:
		# Create the new Order object
		order = Order(
				menu=Menu(pk=request.session['menu']), 
				user=User(pk=request.session['user']), 
				month=now.month, 
				year=now.year, 
				stripe_token=request.session['stripe_token']
		)
		order.save()

		# Update the UserProfile
		#bigups http://stackoverflow.com/questions/7498328/how-to-do-a-reverse-foreignkey-lookup-for-all-records-in-django
		profile = Profile.objects.get(user=request.session['user'])
		profile.subscribed = True
		profile.menu = request.session['menu']
		profile.last_4_digits = request.session['last_4_digits']
		profile.save()

		# Reset the keys
		del request.session['menu']
		del request.session['user']
		del request.session['last_4_digits']
		del request.session['stripe_token']

		# Success message
		return HttpResponse('Success! You are order #%s. Go <a href="/">home</a>' % order.id)
	else:
		return HttpResponseRedirect('/order/')

"""
ORDER FLOW

index -> order form / register form / shipping form / payment form / preferences form -> success page -> success email


/order
	input: menu selection
	redirect -> /register
/accounts/signup
	input: username, email, password, name, address
	redirect -> /pay
/order/pay
	input: card card info to stripe, last 4 digit, stripe_id
	redirect -> /username/preferences
/accounts/username/preferences
	input: profile selection
/accounts/username/refer
	output: discount code
"""