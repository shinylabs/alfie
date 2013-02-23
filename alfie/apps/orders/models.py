"""
// SHELL CMDS

from alfie.apps.orders.models import *
"""

# time
import datetime
import calendar
now = datetime.datetime.now()

#bigups http://stackoverflow.com/questions/4130922/how-to-increment-datetime-month-in-python
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def subtract_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Import other data models
from alfie.apps.ramens.models import Box

# Import utilities
from alfie.apps.back.shipping.easypostutil import *

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
    price = models.IntegerField(max_length=7) # price in pennies
    notes = models.TextField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class OrderManager(models.Manager):
    # SELECTORS
    def this_month(self, now=now):
        """
        Orders are only valid if:
            - subscribed is not null or blank
            - address_verified is True
            - stripe_token is not null or blank
            - killed is null
            - overdue is False
            - cancelled is null
        """
        return self.filter(year=now.year).filter(month=now.month)

    def prev_month(self, now=now):
        now = subtract_months(now, 1)
        return self.filter(year=now.year).filter(month=now.month)

    def quarterly(self, now=now):
        count = 0
        for i in range(3):
            time = subtract_months(now, i)
            count = count + self.filter(year=time.year).filter(month=time.month)
        return count

    # FINANCES
    def this_month_unpaid(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(paid__isnull=True)

    def this_month_paid(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(paid__isnull=False)

    def prev_month_paid(self, now=now):
        now = subtract_months(now, 1)
        return self.filter(year=now.year).filter(month=now.month).filter(paid__isnull=False)

    def add_lineitem(self, amt, item, orders):
        """
            Takes in amount, lineitem, and order list

            Based on lineitem, affect amount onto orders
        """
        amount = amt / orders.count()
        for order in orders:

            setattr(order, item, amount)
            order.save()

    # HANDLING
    def this_month_to_pack(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(packed__isnull=True)
    def this_month_packed(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(packed__isnull=False)

    def prev_month_packed(self, now=now):
        now = subtract_months(now, 1)
        return self.filter(year=now.year).filter(month=now.month).filter(packed__isnull=False)

    # SHIPPING
    def this_month_manifest(self, now=now):
        list = []
        for i in range(len(zones)):
            dict = {}
            dict['zone'] = i
            dict['orders'] = self.filter(year=now.year).filter(month=now.month).filter(priority=i).count()
            list.append(dict)
        return list

    def this_month_to_ship(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(shipped__isnull=True)

    def this_month_shipped(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(shipped__isnull=False)

    def prev_month_shipped(self, now=now):
        now = subtract_months(now, 1)
        return self.filter(year=now.year).filter(month=now.month).filter(shipped__isnull=False)

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
    user = models.ForeignKey(User, related_name='users')
    choice = models.ForeignKey(Menu, blank=True, null=True)
    box = models.ForeignKey(Box, related_name='orders', blank=True, null=True)
    coupon = models.CharField(max_length=25, blank=True, null=True)
    month = models.IntegerField(max_length=2, blank=True, null=True)
    year = models.IntegerField(max_length=4, blank=True, null=True)

    # Housekeeping
    created = models.DateTimeField(auto_now_add=True, editable=False)
    paid = models.DateTimeField(blank=True, null=True)
    packed = models.DateTimeField(blank=True, null=True)
    shipped = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, editable=False)
    notes = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    # Payment info
    last4 = models.IntegerField(max_length=4, blank=True, null=True)
    payment_attempts = models.IntegerField(blank=True, null=True)
    last_payment_attempt = models.DateTimeField(blank=True, null=True, editable=False)

    # Bookkeeping
    #tasks default these to 0
    product_cost = models.IntegerField(max_length=7, blank=True, null=True)
    prize_cost = models.IntegerField(max_length=7, blank=True, null=True)
    prints_cost = models.IntegerField(max_length=7, blank=True, null=True)
    packaging_cost = models.IntegerField(max_length=7, blank=True, null=True)
    shipping_cost = models.IntegerField(max_length=7, blank=True, null=True)
    stripe_fee = models.IntegerField(max_length=7, blank=True, null=True)

    objects = OrderManager()

    def check_card(self):
        """
            Call up Stripe API and save last4
        """
        import stripe
        from django.conf import settings
        stripe.api_key = settings.TEST_STRIPE_API_KEY

        cust_id = self.user.profile.stripe_cust_id
        resp = stripe.Charge.all(customer=cust_id)

        if resp['data'][0]['card']['last4']:
            self.last4 = resp['data'][0]['card']['last4'];
            self.save()        

    def check_paid(self):
        """
            Call up Stripe API and verify if order has been paid, else charge order, then update Order object
        """
        import stripe
        from django.conf import settings
        stripe.api_key = settings.TEST_STRIPE_API_KEY

        cust_id = self.user.profile.stripe_cust_id
        resp = stripe.Charge.all(customer=cust_id)

        if resp['data'][0]['paid'] is True:
            self.paid = now;
            self.save()

    def check_stripe_fee(self):
        """
            Call up Stripe API and save last4
        """
        import stripe
        from django.conf import settings
        stripe.api_key = settings.TEST_STRIPE_API_KEY

        cust_id = self.user.profile.stripe_cust_id
        resp = stripe.Charge.all(customer=cust_id)

        if resp['data'][0]['fee']:
            self.stripe_fee = resp['data'][0]['fee'];
            self.save()

    def check_costs(self):
        total = (self.product_cost if self.product_cost is not None else 0)
        total += (self.prize_cost if self.prize_cost is not None else 0)
        total += (self.prints_cost if self.prints_cost is not None else 0) 
        total += (self.packaging_cost if self.packaging_cost is not None else 0) 
        total += (self.shipping_cost if self.shipping_cost is not None else 0) 
        total += (self.stripe_fee if self.stripe_fee is not None else 0)
        return total

    def check_cutoff(self):
        """
            If past cutoff datetime then push to next month
            Else save for current month, year and send to shipping queue

            #policy - cutoff is 7 days before last day of the month
        """
        import calendar     
        #bigups http://stackoverflow.com/questions/42950/get-last-day-of-the-month-in-python
        cutoff = calendar.monthrange(self.created.year, now.month)[1] - 7 # 24 < 31
        if self.created.day > cutoff:
            self.year, self.month = self.created.year, self.created.month + 1
        else:
            self.year, self.month = self.created.year, self.created.month

    def got_packed(self):
        """
            Calling this sets self.packed datetimestamp
        """
        if self.paid:
            # set priority
            self.priority = int(verify_zone(str(self.user.profile.ship_state), zones))

            # set packed datetimestamp
            self.packed = now
            self.save()

    def got_shipped(self):
        """
            Calling this sets self.shipped datetimestamp
        """
        if self.packed:
            # buy postage

            # set shipped datetimestamp
            self.shipped = now
            self.save()

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        self.check_cutoff()
        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Order %s for %s' % (self.id, self.user.first_name)

"""

#todo

1. check if order is paid with stripe
2. calc bookkeeping fields


"""