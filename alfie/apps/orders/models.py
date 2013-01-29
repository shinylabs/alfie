# time
import datetime
now = datetime.datetime.now()

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
        sumobox     14          32.00       If you just want to mainline
    """

    name = models.CharField(max_length=128, blank=True, null=True)
    slots = models.CharField(max_length=128, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    notes = models.TextField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class OrderManager(models.Manager):
    def monthly_total(self, month=now.month):
        return self.filter(created__month=month).count()

    def prev_month_total(self):
        pass

    def quarterly_total(self):
        pass

    def pay_queue(self):
        """
        Show queue of orders that need to be paid

        Num of orders paid / num of orders this month

        Num orders paid - num of orders = payment queue
        """
        pass

    def ship_queue(self):
        """
        Show queue of orders that need to be shipped

        Num of orders shipped / num of orders paid

        Num of orders shipped - num of orders paid = # to insert to ship queue 

        Ship queue pulls box fk to see what inventory needs to be pullled

        Ship queue is removed when confirmed as shipped 
        """
        pass

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

    objects = OrderManager()

    def __unicode__(self):
        return u'Order %s for %s' % (self.id, self.user.first_name)