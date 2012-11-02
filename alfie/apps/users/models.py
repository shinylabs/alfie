from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.localflavor.us.models import USStateField

from userena.models import UserenaBaseProfile

import datetime

# https://docs.djangoproject.com/en/dev/topics/auth/

class SubscriberProfile(UserenaBaseProfile):
    # REGISTER
        # email
	    # password
	    # full name
    user = models.OneToOneField(User, unique=True, verbose_name=_('user'), related_name='my_profile')
	
class SubscriberData(models.Model):
    # ship_addr
    ship_address_1 = models.CharField(_("address"), max_length=128, blank=True, null=True)
    ship_address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True, null=True)
    ship_city = models.CharField(_("city"), max_length=64, default="Zanesville", blank=True, null=True)
    ship_state = USStateField(_("state"), default="OH", blank=True, null=True)
    ship_zip_code = models.CharField(_("zip code"), max_length=5, default="43701", blank=True, null=True)

    # bill_addr
    bill_address_1 = models.CharField(_("address"), max_length=128, blank=True, null=True)
    bill_address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True, null=True)
    bill_city = models.CharField(_("city"), max_length=64, default="Zanesville", blank=True, null=True)
    bill_state = USStateField(_("state"), default="OH", blank=True, null=True)
    bill_zip_code = models.CharField(_("zip code"), max_length=5, default="43701", blank=True, null=True)

    # PROFILE
    plan_level = models.CharField(_("plan level"), max_length=255, blank=True, null=True)
    hot_level = models.CharField(_("spice level"), max_length=255, blank=True, null=True)
    allergy = models.CharField(_("allergy"), max_length=255, blank=True, null=True)

    # HOUSEKEEPING
    subscribed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cancelled = models.DateTimeField(blank=True, null=True, editable=False)
    killed = models.DateTimeField(blank=True, null=True, editable=False) # keep for 90 days

	# PAYMENT INFO
    last_4_digits = models.CharField(max_length=4)
    stripe_id = models.CharField(max_length=255)