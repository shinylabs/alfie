from django import forms
from django.forms import ModelForm
from alfie.apps.orders.models import Menu, Order
from alfie.apps.profiles.models import Profile

#bigups http://stackoverflow.com/questions/656614/django-forms-modelchoicefield-using-radioselect-widget-grouped-by-fk
class MenuForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('menu',)

class UserForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('user',)

class OrderForm(forms.ModelForm):
	menu = forms.ModelChoiceField(
		queryset = Menu.objects.all(), 
		widget = forms.RadioSelect(),
		empty_label = None
	)
	class Meta:
		model = Order

class PrefsForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('spice', 'allergy',)


"""
#bigups http://stackoverflow.com/questions/1268209/django-modelform-checkbox-widget
class OrderForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['choice'].widget = forms.RadioSelect(choices=self.fields['choice'].choices)

	class Meta:
		model = Order
"""