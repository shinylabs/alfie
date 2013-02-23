"""
// SHELL CMDS

from alfie.apps.profiles.models import *
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.localflavor.us.models import USStateField

# Import other models
from userena.models import UserenaBaseProfile
from alfie.apps.orders.models import Menu

# Import EasyPost
import easypost.easypost
easypost.easypost.api_key = '8xc2JMjUQp9PwQMDsjXBy62sp-uzUC4g'

class Profile(UserenaBaseProfile):
    """
    Creates a Profile object keyed to a User object that defines user profile information.

    """
    # Keyed to User object
    # fields=email, password, firstname, lastname
    #user = models.OneToOneField(User, unique=True, verbose_name=_('user'), related_name='profile')
    user = models.OneToOneField(User)

    # Menu choice
    # this is unique from Order.menu because customer can upgrade/downgrade so this determines next month's auto-bill
    choice = models.ForeignKey(Menu, blank=True, null=True)

    # shipping address
    ship_address_1 = models.CharField(_("Address"), max_length=128, blank=True, null=True)
    ship_address_2 = models.CharField(_("Address cont'd"), max_length=128, blank=True, null=True)
    ship_city = models.CharField(_("City"), max_length=64, blank=True, null=True)
    ship_state = USStateField(_("State"), blank=True, null=True)
    ship_zip_code = models.CharField(_("Zip code"), max_length=5, blank=True, null=True)
    address_verified = models.NullBooleanField()
    shipping_rate = models.IntegerField(max_length=7, blank=True, null=True)

    # Preferences
    #bigups http://stackoverflow.com/questions/2726476/django-multiple-choice-field-checkbox-select-multiple
    #bigups https://docs.djangoproject.com/en/dev/ref/models/fields/#field-choices
    CATS = 'C'
    DOGS = 'D'
    BABIES = 'B'
    CUTE_CHOICES = (
        (CATS, 'Cats'),
        (DOGS, 'Dogs'),
        (BABIES, 'Babies'), 
    )

    SPICY_LEVEL_1 = 'S1'
    SPICY_LEVEL_2 = 'S2'
    SPICY_LEVEL_3 = 'S3'
    SPICY_LEVEL_4 = 'S4'
    SPICY_LEVEL_CHOICES = (
        (SPICY_LEVEL_1, 'Meh'),
        (SPICY_LEVEL_2, 'Miami'),
        (SPICY_LEVEL_3, 'Three Alarm'),
        (SPICY_LEVEL_4, 'Jeremy Lin')
    )

    SHELLFISH = 'A1'
    GLUTEN = 'A2'
    MILK = 'A3'
    MSG = 'A4'
    PEANUT = 'A5'
    SOY = 'A6'
    OTHER = 'A7'
    ALLERGY_TYPE_CHOICES = (
        (SHELLFISH, 'Shellfish'),
        (GLUTEN, 'Gluten'),
        (MILK, 'Milk'),
        (MSG, 'MSG'),
        (PEANUT, 'Peanut'),
        (SOY, 'Soy'),
        (OTHER, 'Other')
    )

    cutest = models.CharField(_("cuter"), max_length=1, choices=CUTE_CHOICES, blank=True, null=True)
    spicy = models.CharField(_("spice level"), max_length=2, choices=SPICY_LEVEL_CHOICES, blank=True, null=True)
    allergy = models.CharField(_("allergy"), max_length=2, choices=ALLERGY_TYPE_CHOICES, blank=True, null=True)

    # Housekeeping
    created = models.DateTimeField(auto_now_add=True, editable=False)
    subscribed = models.DateTimeField(blank=True, null=True)
    cancelled = models.DateTimeField(blank=True, null=True)
    killed = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, editable=False)
    notes = models.CharField(max_length=255, blank=True, null=True)

	# Payment info
    stripe_cust_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_token = models.CharField(max_length=255, blank=True, null=True)
    last4 = models.IntegerField(max_length=4, blank=True, null=True)
    overdue = models.BooleanField(default=False)

    def get_addr_values(self):
        return [self.ship_address_1, self.ship_address_2, self.ship_city, self.ship_state, self.ship_zip_code]

    def get_addr(self):
        if self.ship_address_2 is None:
            addr = {"street1": self.ship_address_1, "city": self.ship_city, "state": self.ship_state, "zip": self.ship_zip_code}
        else:
            addr = {"street1": self.ship_address_1, "street2": self.ship_address_2, "city": self.ship_city, "state": self.ship_state, "zip": self.ship_zip_code}
        return addr

    def get_pref(self):
        return {"cutest": self.cutest, "spicy": self.spicy, "allergy": self.allergy}

    def create_address(self):
        return easypost.easypost.Address(self.user.first_name + ' ' + self.user.last_name, **self.get_addr())

    def verify_address(self):
        try:
            self.create_address().verify()
            self.address_verified = True
        except:
            self.address_verified = False