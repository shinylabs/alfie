from django import forms
from django.utils.translation import ugettext_lazy as _
# https://docs.djangoproject.com/en/dev/ref/contrib/localflavor/#united-states-of-america-us
from django.contrib.localflavor.us.forms import *
from alfie.apps.users.models import SubscriberData

from userena.forms import SignupForm

class SignupFormExtra(SignupForm):
    """ 
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.
    """
    first_name = forms.CharField(label=_(u'First name'), max_length=30, required=False)
    last_name = forms.CharField(label=_(u'Last name'), max_length=30, required=False)


    def save(self):
        """ 
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()

        user_profile = new_user.get_profile()
        """
        user_profile.ship_address_1 = self.cleaned_data['ship_address_1']
        user_profile.ship_address_2 = self.cleaned_data['ship_address_2']
        user_profile.ship_city = self.cleaned_data['ship_city']
        user_profile.ship_state = self.cleaned_data['ship_state']
        user_profile.ship_zip_code = self.cleaned_data['ship_zip_code']
        """
        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        return new_user

PLAN_LEVEL = (
    ('s', 'Small'),
    ('m', 'Medium'),
    ('l', 'Large'),
)

HOT_LEVEL = (
    ('1', 'Meh'),
    ('2', 'Miami'),
    ('3', 'Four Alarm'),
    ('4', 'Jeremy Lin'),
)

ALLERGY = (
    ('s', 'shellfish'),
    ('g', 'gluten'),
    ('k', 'milk'),
    ('p', 'peanut'),
    ('m', 'msg'),
    ('o', 'other'),
)

class SubDataForm(forms.Form):
    # PAYMENT
    # ship_addr
    ship_address_1 = forms.CharField(label=_(u"address"), max_length=128)
    ship_address_2 = forms.CharField(label=_(u"address cont'd"), max_length=128)
    ship_city = forms.CharField(label=_(u"city"), max_length=64)
    ship_state = USStateField(label=_(u"state"))
    ship_zip_code = forms.CharField(label=_(u"zip code"), max_length=5)

    # bill_addr
    bill_address_1 = forms.CharField(label=_(u"address"), max_length=128)
    bill_address_2 = forms.CharField(label=_(u"address cont'd"), max_length=128)
    bill_city = forms.CharField(label=_(u"city"), max_length=64)
    bill_state = USStateField(label=_(u"state"))
    bill_zip_code = forms.CharField(label=_(u"zip code"), max_length=5)

    # PROFILE
    plan_level = forms.CharField(label=_(u"plan level"), max_length=255)
    hot_level = forms.CharField(label=_(u"spice level"), max_length=255)
    allergy = forms.CharField(label=_(u"allergy"), max_length=255)