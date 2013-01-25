from django import forms
from django.forms.formsets import formset_factory
from alfie.apps.ramens.models import Box

class BoxForm(forms.ModelForm):
	class Meta:
		model = Box
		exclude = ('cost',)

#bigups https://docs.djangoproject.com/en/dev/topics/forms/formsets/
BoxFormSet = formset_factory(BoxForm, extra=3)