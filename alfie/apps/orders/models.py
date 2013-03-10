from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Import other data models
from alfie.apps.ramens.models import Box

# time helpers
from alfie.apps.back.timehelpers import *
"""
    Imports in:
    datetime
    add_months()
    subtract_months()
"""

# stripe
import stripe
from django.conf import settings
stripe.api_key = settings.TEST_STRIPE_API_KEY
# stripe helpers
from alfie.apps.back.finance.stripeutil import *

# Import EasyPost
import easypost.easypost
from django.conf import settings
easypost.easypost.api_key = settings.TEST_EASYPOST_API_KEY

# Where to store postage files
MEDIA_PATH = 'alfie/media/'
POSTAGE_FILE_PATH = 'assets/postage/'

# USPS Zones and Transit
# http://www.survivalsuppliers.com/images/zone_map.gif
# N-CA zip codes http://info.kaiserpermanente.org/steps/zipcodes_nocal.html
# S-CA zip codes http://info.kaiserpermanente.org/steps/zipcodes_socal.html
# W-NV zip codes http://www.mongabay.com/igapo/zip_codes/counties/alpha/Nevada%20County-California1.html
# W-PA zip codes
# E-PA zip codes

zone0 = ['CA', 'NV'] # 1 day
zone1 = ['CA', 'WA', 'OR', 'ID', 'NV', 'UT'] # 2 days
zone2 = ['MT', 'WY', 'CO', 'AZ', 'NM'] # 3 days
zone3 = ['ND', 'NE', 'KS', 'OK', 'TX', 'IA', 'MO', 'AR', 'WI', 'IL', 'IN', 'MI'] # 4 days
zone4 = ['SD', 'MN', 'OH', 'KY', 'TN', 'MS', 'LA', 'WV', 'PA', 'NY'] # 5 days
zone5 = ['ME', 'VT', 'NH', 'MA', 'CT', 'RI', 'NJ', 'MD', 'DE', 'DC', 'VA', 'NC', 'SC', 'GA', 'AL', 'FL'] # 6 days
zone6 = ['AL', 'HI'] # 7 days

zones = [{'zone': '0', 'states': zone0, 'transit': '1 day'}, 
         {'zone': '1', 'states': zone1, 'transit': '2 days'},
         {'zone': '2', 'states': zone2, 'transit': '3 days'},
         {'zone': '3', 'states': zone3, 'transit': '4 days'},
         {'zone': '4', 'states': zone4, 'transit': '5 days'},
         {'zone': '5', 'states': zone5, 'transit': '6 days'},
         {'zone': '6', 'states': zone6, 'transit': '7 days'}]

class Menu(models.Model):
    """
    Creates a Menu object that defines LuckyRamenCat menu options.

    Initial data:
        _name_      _slots_     _price_     _notes_
        tinybox     4           1200        For people that want to try
        bigbox      8           2200        For the ramen fanatic
        sumobox     14          3200        If you just want to mainline
    """
    name = models.CharField(max_length=128, blank=True, null=True)
    slots = models.IntegerField(max_length=128, blank=True, null=True)
    price = models.IntegerField(max_length=7) # price in pennies
    notes = models.TextField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class OrderManager(models.Manager):
    # Helpers
    def get_costs_fields(self):
        return [field.name for field in self._meta.fields if field.name.endswith('cost') or field.name.endswith('fee')]

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
    def check_last4(self, now=now):
        for order in self.filter(year=now.year).filter(month=now.month):
            order.check_last4()

    def check_paid(self, now=now):
        for order in self.filter(year=now.year).filter(month=now.month):
            order.check_paid()

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
        return self.filter(year=now.year).filter(month=now.month).filter(paid__isnull=False).filter(packed__isnull=True)
    def this_month_packed(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(paid__isnull=False).filter(packed__isnull=False)

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
        return self.filter(year=now.year).filter(month=now.month).filter(packed__isnull=False).filter(shipped__isnull=True)

    def this_month_shipped(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(packed__isnull=False).filter(shipped__isnull=False)

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
    user = models.ForeignKey(User, related_name='orders')
    choice = models.ForeignKey(Menu, blank=True, null=True)
    box = models.ForeignKey(Box, related_name='orders', blank=True, null=True)
    coupon = models.CharField(max_length=25, blank=True, null=True)
    month = models.IntegerField(max_length=2, blank=True, null=True)
    year = models.IntegerField(max_length=4, blank=True, null=True)

    # Shipping/Handling
    packed = models.DateTimeField(blank=True, null=True)
    shipped = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    tracker = models.CharField(max_length=50, blank=True, null=True)
    label_url = models.URLField(blank=True, null=True)
    label_file = models.ImageField(upload_to=POSTAGE_FILE_PATH, blank=True, null=True)

    # Payment info
    last4 = models.IntegerField(max_length=4, blank=True, null=True)
    paid = models.DateTimeField(blank=True, null=True)
    last_payment_attempt = models.DateTimeField(blank=True, null=True, editable=False)
    payment_attempts = models.IntegerField(blank=True, null=True)
    refunded = models.DateTimeField(blank=True, null=True)

    # Bookkeeping
    product_cost = models.IntegerField(max_length=7, blank=True, null=True, default=0)
    prize_cost = models.IntegerField(max_length=7, blank=True, null=True, default=0)
    prints_cost = models.IntegerField(max_length=7, blank=True, null=True, default=0)
    packaging_cost = models.IntegerField(max_length=7, blank=True, null=True, default=0)
    shipping_cost = models.IntegerField(max_length=7, blank=True, null=True, default=0)
    stripe_fee = models.IntegerField(max_length=7, blank=True, null=True, default=0)

    # Housekeeping
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    notes = models.CharField(max_length=255, blank=True, null=True)
    killed = models.DateTimeField(blank=True, null=True)

    objects = OrderManager()

    def check_card(self):
        """
            Call up Stripe API and save last4
        """
        if not self.user.profile.stripe_cust_id:
            if create_customer(self.user, self.user.profile):
                self.check_card()
            else: print 'Not a stripe customer'
        else:
            resp = stripe.Charge.all(customer=self.user.profile.stripe_cust_id)

            if resp['data'][-1]['card']['last4']:
                self.last4 = resp['data'][0]['card']['last4']
                self.save()     

    def check_paid(self):
        """
            Call up Stripe API and verify if order has been paid, else charge order, then update Order object
        """
        if not self.user.profile.stripe_cust_id:
            if create_customer(self.user, self.user.profile):
                self.check_paid()
            else: print 'Not a stripe customer'
        else:
            resp = stripe.Charge.all(customer=self.user.profile.stripe_cust_id)

            if resp['data'][-1]['paid']:
                self.paid = now
                self.stripe_fee = resp['data'][-1]['fee']
                self.save()
            else:
                self.last_payment_attempt = now
                check_overdue(self.user.profile)
                self.save()

    def set_stripe_fee(self):
        """
            Call up Stripe API and save last4
        """
        if not self.user.profile.stripe_cust_id:
            if create_customer(self.user, self.user.profile):
                self.check_stripe_fee()
            else: print 'Not a stripe customer'
        else:
            resp = stripe.Charge.all(customer=self.user.profile.stripe_cust_id)

            if resp['data'][-1]['fee']:
                self.stripe_fee = resp['data'][-1]['fee']
                self.save()

    def set_product_cost(self):
        """
            Save order.box.cost
        """
        if self.box.cost:
            self.product_cost = self.box.cost
            self.save()

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

    def create_shipment(self):
        homebase = {'name': 'LuckyRamenCat', 'street1': '7150 Rainbow Drive', 'state': 'CA', 'zip': '95129', 'city': 'San Jose'}
        from_address = easypost.easypost.Address(**homebase)
        #todo check address_verified
        to_address = self.user.profile.create_address()
        package = self.box.create_package()
        return easypost.easypost.Shipment(to_address, from_address, package)

    def check_rates(self):
        shipment = self.create_shipment()
        rates = shipment.rates()
        #todo add transit time data
        print '\nShipping to %s' % (self.user.profile.ship_state)
        for rate in rates:
            print rate.carrier, rate.service, rate.price
        return rates

    def set_shipping_cost(self, preferred_service='ParcelSelect'):
        try:
            rates = self.check_rates()
            for rate in rates:
                if rate.service == preferred_service:
                    self.shipping_cost = int(float(rate.price) * 100)
                    self.user.profile.shipping_rate = int(float(rate.price) * 100)
                    self.save()
        except Exception, e:
            print str(e)
            return False

    def create_postage(self, preferred_service='ParcelSelect'):
        shipment = self.create_shipment()
        rates = self.check_rates()
        for preferred_rate in rates:
            if preferred_rate.service == preferred_service:
                rate = preferred_rate
        return easypost.easypost.Postage(shipment, rate)

    def buy_postage(self):
        try:
            postage = self.create_postage()
            postage.buy()
            self.tracker = postage.tracking_code
            self.label_url = postage.label_url
            #self.label_file = postage.label_file_name
            self.save()
        except Exception, e:
            print str(e)
            return False

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

    def get_costs_fields(self):
        # return a list of field/values
        #bigups http://www.djangofoo.com/80/get-list-model-fields
        return [field.name for field in Order._meta.fields if field.name.endswith('cost') or field.name.endswith('fee')]

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        self.check_cutoff()
        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Order %s for %s' % (self.id, self.user.first_name)