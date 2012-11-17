import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# https://docs.djangoproject.com/en/dev/topics/auth/

class Menu(models.Model):
    """
    Creates a Menu object that defines LuckyRamenCat menu options.

    Initial data:
        _name_      _size_      _price_     _notes_
        tinybox     4           11.99       For people that want to try
        bigbox      8           21.99       For the ramen fanatic
        sumobox     16          31.99       If you just want to mainline
    """

    name = models.CharField(max_length=128, blank=True, null=True)
    size = models.CharField(max_length=128, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    notes = models.TextField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class Order(models.Model):
    """
    Creates a Order object that defines an order to be filled and shipped.

    Initial data:
        _choice_    _user_      _month_     _year_
        0           23          12          2012
        0           25          12          2012
        1           32          12          2012
        1           48          12          2012
        2           102         01          2013
    """

    choice = models.ForeignKey(Menu) #task rename to menu
    user = models.ForeignKey(User, blank=True, null=True)
    # pack = models.ForeignKey(Ramen) #task create then link to ramen app
    month = models.CharField(max_length=2, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    # Housekeeping
    payment_attempt = models.IntegerField(blank=True, null=True)
    last_payment_attempt = models.DateTimeField(blank=True, null=True, editable=False)
    order_timestamp = models.DateTimeField(blank=True, null=True, editable=False) #task auto_now_add=True, 
    ship_timestamp = models.DateTimeField(blank=True, null=True, editable=False)

    # Payment info
    last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.id)