from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import datetime

# https://docs.djangoproject.com/en/dev/topics/auth/

class Menu(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    size = models.CharField(max_length=128, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    notes = models.TextField(max_length=255, blank=True, null=True)

    def __unicode__(self):
		return self.name

class Order(models.Model):
    # rename to choice
    plan = models.ForeignKey(Menu)
    user = models.ForeignKey(User, blank=True, null=True)
    # pack = models.ForeignKey(Ramen)
    month = models.CharField(max_length=2, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    # HOUSEKEEPING
    payment_attempt = models.IntegerField(blank=True, null=True)
    last_payment_attempt = models.DateTimeField(blank=True, null=True, editable=False)
    order_timestamp = models.DateTimeField(blank=True, null=True, editable=False) # auto_now_add=True, 
    ship_timestamp = models.DateTimeField(blank=True, null=True, editable=False)