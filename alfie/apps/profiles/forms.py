from django import forms
from django.utils.translation import ugettext_lazy as _
# https://docs.djangoproject.com/en/dev/ref/contrib/localflavor/#united-states-of-america-us
from django.contrib.localflavor.us.forms import *
from alfie.apps.profiles.models import Profile
from userena.forms import SignupForm

class SignupFormExtra(SignupForm):
    """ 
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.
    """
    first_name = forms.CharField(label=_(u'First name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last name'), max_length=30)

    # shipping address
    ship_address_1 = forms.CharField(label=_(u"Address"), max_length=128)
    ship_address_2 = forms.CharField(label=_(u"Address cont'd"), max_length=128, required=False)
    ship_city = forms.CharField(label=_(u"City"), max_length=64)
    ship_state = USStateField(label=_(u"State"))
    ship_zip_code = forms.CharField(label=_(u"Zip code"), max_length=5)

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
        user_profile.ship_address_1 = self.cleaned_data['ship_address_1']
        user_profile.ship_address_2 = self.cleaned_data['ship_address_2']
        user_profile.ship_city = self.cleaned_data['ship_city']
        user_profile.ship_state = self.cleaned_data['ship_state']
        user_profile.ship_zip_code = self.cleaned_data['ship_zip_code']

        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        return new_user

SPICE_LEVEL = (
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

class PrefForm(forms.Form):
    # PROFILE
    spice = forms.CharField(label=_(u"spice level"), max_length=255)
    allergy = forms.CharField(label=_(u"allergy"), max_length=255)