from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from alfie.apps.users.forms import SubDataForm

def signup(request):
	return HttpResponse('signup as new user -> <a href="/signup">signup</a>')

def login(request):
	return HttpResponse('login -> <a href="/login">login</a>')

def logout(request):
	return HttpResponse('logout-> <a href="/logout">logout</a>')

def subdata(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SubDataForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = SubDataForm() # An unbound form
    return render_to_response('users/data_form.html', {'form': form,}, context_instance=RequestContext(request))

def paydata(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SubDataForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = SubDataForm() # An unbound form
    return render_to_response('users/pay_form.html', {'form': form,}, context_instance=RequestContext(request))


"""

LOGIN FLOW

index -> login -> view profile -> edit profile, cancel, upgrade, history

"""