from django import forms
from django.forms import ModelForm
from alfie.apps.orders.models import Menu, Order
from alfie.apps.profiles.models import Profile, Cutelist

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

cutelist = (('1', 'cats'), 
			('2', 'dogs'),
			('3', 'babies'))

spicelist = (('small', 'small'), 
			('medium', 'medium'),
			('hot', 'hot'),
			('jeremy lin', 'jeremy lin'))

allerglist = (('shellfish', 'shellfish'), 
			  ('gluten', 'gluten'),
			  ('spices', 'spices'),
			  ('milk', 'milk'),
			  ('soy', 'soy'),
			  ('msg', 'msg'))

class PrefsForm(forms.ModelForm):
	#cutelist = forms.ModelChoiceField(queryset=Cutelist.objects.all(), required=False, widget=forms.RadioSelect)
	cuter = forms.ChoiceField(choices=cutelist, widget=forms.RadioSelect)
	spicy = forms.ChoiceField(choices=spicelist, widget=forms.RadioSelect)
	allergies = forms.ChoiceField(choices=allerglist, widget=forms.CheckboxSelectMultiple)

	class Meta:
		model = Profile
		fields = ['spicy', 'allergies', 'cuter']


"""
#bigups http://stackoverflow.com/questions/1268209/django-modelform-checkbox-widget
class OrderForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['choice'].widget = forms.RadioSelect(choices=self.fields['choice'].choices)

	class Meta:
		model = Order
"""