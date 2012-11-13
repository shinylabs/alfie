from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from alfie.apps.orders.forms import OrderForm
from alfie.apps.users.forms import SignupFormExtra

def showMenu(request):
	"""
		Shows off menu choices
	
		Input: selection
		Output: modelform
	"""
	choice = ''
	if request.method == 'POST': # If the form has been submitted...
		form = OrderForm(request.POST) # A form bound to the POST data
		choice = form.data['menu']
		form = SignupFormExtra()
#		return HttpResponse('you chose %s -> now register <a href="/accounts/signup">user form</a>' % choice) # Redirect after POST
	else:
		orderform = OrderForm() # An unbound form
		signupform = SignupFormExtra()
	return render_to_response('orders/order_form.html', {'orderform': orderform, 'signupform': signupform, 'choice': choice}, context_instance=RequestContext(request))

def startOrder(request):
	"""
		Takes customer and payment info
		
		Input: new user, new payment
		Output: preferences form
	"""
	pass

def saveOrder(request):
	"""
		Validate and saves order, bills order, sends email
		
		Input: user obj, payment obj
		Output: order obj, redirect to success page
	"""
	pass


"""

ORDER FLOW

index -> order form / register form / shipping form / payment form / preferences form -> success page -> success email


/order
	input: menu selection
	redirect -> /register
/register
	input: username, email, password, name, address
	redirect -> /pay
/pay
	input: card card info to stripe, last 4 digit, stripe_id
	redirect -> /username/preferences
/accounts/username/preferences
	input: profile selection
/accounts/username/refer
	output: discount code
"""