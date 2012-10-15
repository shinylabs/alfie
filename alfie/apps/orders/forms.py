from django.forms import ModelForm
from alfie.apps.orders.models import Order, OrderChoice
from django import forms

class OrderForm(ModelForm):
	class Meta:
		model = Order

#bigups http://stackoverflow.com/questions/656614/django-forms-modelchoicefield-using-radioselect-widget-grouped-by-fk
class StartOrderForm(ModelForm):
	level = forms.ModelChoiceField(
		queryset = OrderChoice.objects.all(), 
		widget = forms.RadioSelect,
		empty_label = None
	)
	class Meta:
		model = Order
		fields = ('level',)