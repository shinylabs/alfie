# python
import datetime
now = datetime.datetime.now()

# django
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

# data
from django.contrib.auth.models import User
from alfie.apps.users.models import UserProfile
from alfie.apps.orders.models import Menu, Order

# forms
from alfie.apps.orders.forms import OrderForm, ChoiceForm, UserForm
from alfie.apps.users.forms import SignupFormExtra


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
		form = ChoiceForm(request.POST)
		# What is the choice from form
		choice = form.data['choice']
		# Set session variable
		request.session['choice'] = choice
		# Check if user status
		if request.user.is_authenticated():
			auth = True
		else:
			auth = False
		#return HttpResponse('You chose %s. User auth is %s. Now <a href="/accounts/signup">sign up</a> or <a href="/accounts/signin">sign in</a>.' % (choice, auth))
		return HttpResponseRedirect('/accounts/signup')
	# Initialize forms
	else:
		if 'choice' in request.session:
			if 'user_id' in request.session:
				return HttpResponseRedirect('/order/pay')
			else:
				choice = request.session['choice']
				#return HttpResponse('You already selected %s. <a href="/order/cancel">Cancel order</a>? <a href="/accounts/signup">Sign up</a>?' % choice)
				return HttpResponseRedirect('/accounts/signup')
		else:
			# Some unbound forms
			orderform = OrderForm()
			choiceform = ChoiceForm()
			userform = UserForm()
			return render_to_response('orders/order_form.html', {'orderform': orderform, 'choiceform': choiceform, 'userform': userform}, context_instance=RequestContext(request))		

def cancelOrder(request):
	# Reset variable in session
	if 'choice' in request.session:
		del request.session['choice']
	if 'user_id' in request.session:
		del request.session['user_id']
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
		if request.user.is_authenticated():
			auth = True
		else:
			auth = False
		if 'choice' not in request.session or 'user_id' not in request.session:
			return HttpResponseRedirect('/order/')
		else:
			choice = request.session['choice']
			user = request.session['user_id']
			price = Menu.objects.get(pk=choice).price
			return render_to_response('orders/payment.html', {'choice': choice, 'price': price, 'auth': auth, 'user': user}, context_instance=RequestContext(request))

def saveOrder(request):
	if 'choice' in request.session:
		# Create the new Order object
		order = Order(
				choice=Menu(pk=request.session['choice']), 
				user=User(pk=request.session['user_id']), 
				month=now.month, 
				year=now.year, 
				order_timestamp=datetime.datetime.now(),
				last_4_digits=request.session['last_4_digits'], 
				stripe_id=request.session['stripe_token']
		)
		order.save()

		# Update the UserProfile
		#bigups http://stackoverflow.com/questions/7498328/how-to-do-a-reverse-foreignkey-lookup-for-all-records-in-django
		profile = UserProfile.objects.get(user=request.session['user_id'])
		profile.subscribed = True
		profile.choice = request.session['choice']
		profile.last_4_digits = request.session['last_4_digits']
		profile.stripe_id = request.session['stripe_token']
		profile.save()

		# Reset the keys
		del request.session['choice']
		del request.session['user_id']
		del request.session['last_4_digits']
		del request.session['stripe_token']

		# Success message
		return HttpResponse('Success! You are order #%s' % order.id)
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