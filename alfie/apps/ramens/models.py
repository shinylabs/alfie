from django.db import models
from django.utils.translation import ugettext as _

class Manufacturer(models.Model):
	name = models.CharField(max_length=128, blank=True, null=True)
	address = models.TextField(max_length=255, blank=True, null=True)
	website = models.URLField(max_length=255, blank=True, null=True)
	origin = models.CharField(max_length=128, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.name)

class Flavor(models.Model):
	taste = models.CharField(max_length=128, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.taste)

class Review(models.Model):
	notes = models.TextField(max_length=255, blank=True, null=True)
	# rating # switch to https://github.com/dcramer/django-ratings
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)

class Ramen(models.Model):
	name = models.CharField(max_length=128, blank=True, null=True)
	price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
	notes = models.TextField(max_length=255, blank=True, null=True)
	upc = models.IntegerField(max_length=128, blank=True, null=True)
	mfg = models.ForeignKey(Manufacturer, blank=True, null=True)
	weight = models.CharField(max_length=128, blank=True, null=True)
	dimensions = models.CharField(max_length=128, blank=True, null=True)
	description = models.TextField(max_length=255, blank=True, null=True)
	directions = models.TextField(max_length=255, blank=True, null=True)
	nutrition = models.TextField(max_length=255, blank=True, null=True)
	ingredients = models.TextField(max_length=255, blank=True, null=True)
	flavors = models.ManyToManyField(Flavor, blank=True, null=True)
	reviews = models.ManyToManyField(Review, blank=True, null=True)
	ratings = models.IntegerField(blank=True, null=True)
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)

	def __unicode__(self):
		return u'%s' % (self.name)

class Box(models.Model):
	ramens = models.ManyToManyField(Ramen, through='Membership')
	month = models.CharField(max_length=2)
	year = models.CharField(max_length=4)
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)

	def __unicode__(self):
		return u'%s - %s' % (self.month, self.year)

	class Meta:
		verbose_name_plural = "boxes"

class Membership(models.Model):
	ramen = models.ForeignKey(Ramen)
	box = models.ForeignKey(Box)
	notes = models.TextField(max_length=255, blank=True, null=True)
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)

#tasks create abstract base classes for housekeeping purposes
#bigups https://docs.djangoproject.com/en/dev/topics/db/models/#abstract-base-classes
# name, created

#notes
# django model _meta https://django-model-_meta-reference.readthedocs.org/en/latest/