from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from alfie.apps.orders.forms import OrderForm, ChoiceForm, UserForm
from alfie.apps.orders.models import Menu
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
		return HttpResponse('payment posted')
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
	pass

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