from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Import other models
from alfie.apps.ramens.models import Box

class Menu(models.Model):
    """
    Creates a Menu object that defines LuckyRamenCat menu options.

    Initial data:
        _name_      _slots_     _price_     _notes_
        tinybox     4           12.00       For people that want to try
        bigbox      8           22.00       For the ramen fanatic
        sumobox     16          32.00       If you just want to mainline
    """

    name = models.CharField(max_length=128, blank=True, null=True)
    slots = models.CharField(max_length=128, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    notes = models.TextField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class Order(models.Model):
    """
    Creates a Order object that defines an order to be filled and shipped.

    Initial data:
        _id_        _choice_    _user_      _box.month_     _box.year_
        1           0           23          12              2012
        2           0           25          12              2012
        3           1           32          12              2012
        4           1           48          12              2012
        5           2           102         01              2013
    """
    user = models.ForeignKey(User, related_name='orders')
    choice = models.ForeignKey(Menu, blank=True, null=True)
    box = models.ForeignKey(Box, blank=True, null=True)
    coupon = models.CharField(max_length=25, blank=True, null=True)

    # Housekeeping
    created = models.DateTimeField(auto_now_add=True, editable=False)
    gotpaid = models.DateTimeField(blank=True, null=True)
    shipped = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, editable=False)
    notes = models.CharField(max_length=255, blank=True, null=True)

    # Payment info
    last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    payment_attempts = models.IntegerField(blank=True, null=True)
    last_payment_attempt = models.DateTimeField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return u'Order %s for %s' % (self.id, self.user.first_name)