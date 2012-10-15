from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import datetime

# https://docs.djangoproject.com/en/dev/topics/auth/
	
class OrderChoice(models.Model):
	size = models.CharField(max_length=128, blank=True, null=True)
	name = models.CharField(max_length=128, blank=True, null=True)
	price = models.CharField(max_length=128, blank=True, null=True)
    # price = models.DecimalField( decimal_places=2, max_digits=7 )
	notes = models.TextField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return self.name

class Order(models.Model):
    level = models.ForeignKey(OrderChoice)
    user = models.ForeignKey(User, blank=True, null=True)
    month = models.CharField(max_length=2, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    payment_attempt = models.IntegerField(blank=True, null=True)
    last_payment_attempt = models.DateTimeField(blank=True, null=True, editable=False)
    order_timestamp = models.DateTimeField(blank=True, null=True, editable=False) # auto_now_add=True, 
    ship_timestamp = models.DateTimeField(blank=True, null=True, editable=False)