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

    def this_month_paid(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).exclude(gotpaid__isnull=True)

    def prev_month_paid(self, now=now):
        now = subtract_months(now, 1)
        return self.filter(year=now.year).filter(month=now.month).exclude(gotpaid__isnull=True)

    def pay_orders(self):
        """
            Call up Stripe API and verify if order has been paid, else charge order, then update Order object
        """
        pass

    def unpaid_list(self, now=now):
        """
            Return orders that need to be paid
        """
        return self.filter(year=now.year).filter(month=now.month).filter(gotpaid__isnull=True)

    def this_month_shipped(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).exclude(shipped__isnull=True)

    def unshipped_list(self, now=now):
        """
            Return of orders that need to be shipped

            Ship queue pulls box fk to see what inventory needs to be pullled

            Ship queue is removed when confirmed as shipped 
        """
        return self.filter(year=now.year).filter(month=now.month).filter(shipped__isnull=True)

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
    month = models.IntegerField(max_length=2, blank=True, null=True)
    year = models.IntegerField(max_length=4, blank=True, null=True)

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

    # Bookkeeping
    # product_cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    # prize_cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    # prints_cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    # packaging_cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    # shipping_cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    # stripe_fee = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    objects = OrderManager()

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

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        self.check_cutoff()
        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Order %s for %s' % (self.id, self.user.first_name)