from django import forms
from django.forms import ModelForm
from alfie.apps.orders.models import Menu, Order
from alfie.apps.profiles.models import Profile

#bigups http://stackoverflow.com/questions/656614/django-forms-modelchoicefield-using-radioselect-widget-grouped-by-fk
class OrderForm(forms.ModelForm):
	menu = forms.ModelChoiceField(
			queryset=Menu.objects.all(), 
			widget=forms.RadioSelect(), 
			empty_label=None,
		)
	class Meta:
		model = Order
		fields = ()

class PrefsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cutest', 'spicy', 'allergy',)