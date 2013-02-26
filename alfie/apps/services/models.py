# time
import datetime
now = datetime.datetime.now()

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Import other data models
from alfie.apps.orders.models import Order

"""
    alfie.apps.services

    Admin tools to support customer service functions

     model
          - user fk
          - category
          - resolution
          - created timestamp
          - updated timestamp
          - closed timestamp

     helpers
          - re-ship order
          - refund account
          - cancel account
"""


class ServiceManager(models.Manager):
    def this_month(self, now=now):
        return self.filter(year=now.year).filter(month=now.month)

    def unresolved(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(resolved__isnull=True)

    def resolved(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(resolved__isnull=False)

    def unclosed(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(closed__isnull=True)

    def closed(self, now=now):
        return self.filter(year=now.year).filter(month=now.month).filter(closed__isnull=False)

class Service(models.Model):

    MISSING = 'm'
    REFUND = 'r'
    CANCEL = 'c'
    KILL = 'k'
    OTHER = 'o'
    CAT_CHOICES = (
        (MISSING, 'Missing order'),
        (REFUND, 'Refund order'),
        (CANCEL, 'Cancel order'),
        (KILL, 'Kill account'),
        (OTHER, 'Other')
    )

    user = models.ForeignKey(User, related_name='services')
    order = models.ForeignKey(Order, blank=True, null=True)
    reorder = models.ForeignKey(Order, related_name='reorder', blank=True, null=True)
    issue = models.CharField(max_length=1, choices=CAT_CHOICES, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)    
    resolved = models.DateTimeField(blank=True, null=True)
    closed = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        """
        Service for user.name - Order - Issue - issue.name - Status - ongoing|resolved (timedelta)
        """
        return u'Service for %s - Issue - %s' % (self.user.first_name + ' ' + self.user.last_name, self.get_issue_display())

    def reship(self):
        """
            Create a new order to ship out.
        """
        if self.order.shipped:
            new_order = Order(user=self.user, box=self.order.box)
            new_order.save()
            self.reorder = new_order
            self.resolved = now
            self.save()

    def refund(self):
        """
            Calls backoffice finance tools to apply refund to order 
        """
        if not self.order.shipped:
            # include stripeutil 
            self.order.refunded = now
            self.order.save()
            self.resolved = now
            self.save()

    def cancel(self):
        """
            Cancels orders if before packing or shipping
        """
        if not self.order.packed:
            self.order.killed = now
            self.order.save()
            self.resolved = now
            self.save()

    def kill(self):
        """
            Kills account
        """
        if not self.user.profile.killed:
            self.user.profile.killed = now
            self.user.profile.save()
            self.resolved = now
            self.save()

    def other_resolve(self):
        """
            Resolved a customer issue
        """

    def close(self):
        """
            Closes issue after confirmation from customer
        """
        if self.resolved:
            self.closed = now
            self.save()
