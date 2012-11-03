from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from alfie.apps.orders.forms import OrderForm

def showMenu(request):
	"""
		Shows off menu choices
	
		Input: selection
		Output: modelform
	"""
	if request.method == 'POST': # If the form has been submitted...
		form = OrderForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			plan_selection = form.data['menu']
			return HttpResponse('you chose plan %s -> now register <a href="/accounts/signup">user form</a>' % plan_selection) # Redirect after POST
	else:
		form = OrderForm() # An unbound form
	return render_to_response('orders/order_form.html', {'form': form,}, context_instance=RequestContext(request))

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

index -> order form -> register form / payment form -> pref form -> success page -> success email

"""