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
from alfie.apps.orders.forms import OrderForm, PrefsForm
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
		form = OrderForm(request.POST)
		# What is the choice from form
		menu_choice = form.data['menu']
		# Set session variable
		request.session['menu_choice'] = menu_choice
		return HttpResponseRedirect('/accounts/signup')
	
	# Initialize forms
	else:
		if 'menu_choice' in request.session:
			if 'user' in request.session:
				return HttpResponseRedirect('/order/pay')
			else:
				menu_choice = request.session['menu_choice']
				return HttpResponseRedirect('/accounts/signup')
		else:
			# Some unbound forms
			orderform = OrderForm()
			return render_to_response('orders/order_form.html', {'orderform': orderform}, context_instance=RequestContext(request))		

def cancelOrder(request):
	# Reset variable in session
	if 'menu_choice' in request.session:
		del request.session['menu_choice']
	if 'user' in request.session:
		del request.session['user']
	# Redirect back to function
	return HttpResponseRedirect('/order/')

def payOrder(request):
	if request.method == 'POST':
		# Create the new Order object
		order = Order(
				choice=Menu(pk=request.session['menu_choice']),
				user=User(pk=request.session['user']), 
				stripe_token=request.POST['stripe_token']
		)
		order.save() #tasks set last_4_digits

		# Update the UserProfile
		#bigups http://stackoverflow.com/questions/7498328/how-to-do-a-reverse-foreignkey-lookup-for-all-records-in-django
		profile = Profile.objects.get(user=request.session['user'])
		profile.choice = Menu(pk=request.session['menu_choice'])
		profile.subscribed = now
		profile.save() #tasks set last_4_digits

		# Reset the keys
		del request.session['menu_choice']

		# Success message
		#bigups http://stackoverflow.com/questions/13328810/django-redirect-to-view
		return redirect('alfie.apps.orders.views.savePrefs')
	else:
		if 'menu_choice' not in request.session or 'user' not in request.session:
			return HttpResponseRedirect('/order/')
		else:
			menu_choice = request.session['menu_choice']
			user = request.session['user']
			price = Menu.objects.get(pk=menu_choice).price
			return render_to_response('orders/payment.html', {'menu_choice': menu_choice, 'price': price, 'user': user}, context_instance=RequestContext(request))

def savePrefs(request):
	if request.method == 'POST': 
		# Bound form to POST data
		profile = Profile.objects.get(user=request.session['user'])
		form = PrefsForm(request.POST, instance=profile)
		
		if form.is_valid():
			form.save()
		
		# Reset the keys
		del request.session['user']

		return HttpResponseRedirect('/')
	# Initialize forms
	else:
		prefsform = PrefsForm()
		return render_to_response('orders/prefs_form.html', {'prefsform': prefsform}, context_instance=RequestContext(request))		

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
/order/prefs
	input: profile selection
/order/refer
	output: discount code
"""