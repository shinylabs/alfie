from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from alfie.apps.orders.forms import StartOrderForm

def startorder(request):
    if request.method == 'POST': # If the form has been submitted...
        form = StartOrderForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            plan_selection = form.data['level']
            return HttpResponse('you chose plan %s -> now register <a href="/accounts/signup">user form</a>' % plan_selection) # Redirect after POST
    else:
        form = StartOrderForm() # An unbound form
    return render_to_response('orders/order_form.html', {'form': form,}, context_instance=RequestContext(request))