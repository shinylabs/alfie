from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _
# https://docs.djangoproject.com/en/dev/ref/contrib/localflavor/#united-states-of-america-us
from django.contrib.localflavor.us.forms import *

# Import from other apps
from userena.forms import SignupForm
from alfie.apps.profiles.models import Profile

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

class EditMenuChoiceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('choice',)

    def has_shipped(self, profile):
        """
        Checks if an order has shipped for current month, returns True or False
        """
        import datetime
        now = datetime.datetime.now()

        ship_status = profile.user.orders.all().filter(created__lte=now).order_by('-created')[0].shipped

        if ship_status is None:
            return False
        else:
            return True

class EditPaymentForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('last_4_digits',)

class EditPrefsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('spicy', 'allergy',)
        widgets = {
            'spicy': RadioSelect(),
            'allergy': CheckboxSelectMultiple(attrs={'checked' : 'checked'}),
            }