from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Where to store all the images in devmode
MEDIA_PATH = 'alfie/media/'
RAMEN_FILE_PATH = 'img/ramen/'

class BrandManager(models.Manager):
	def country_count(self, country):
		return self.filter(origin__icontains=country).count()

class Brand(models.Model):
	name = models.CharField(max_length=128, blank=True, null=True)
	address = models.TextField(max_length=255, blank=True, null=True)
	website = models.URLField(max_length=255, blank=True, null=True)
	origin = models.CharField(max_length=128, blank=True, null=True)
	objects = BrandManager()

	def get_absolute_url(self):
		return reverse('brand_detail', args=[self.pk])

	#bigups http://stackoverflow.com/questions/2217478/django-templates-loop-through-and-print-all-available-properties-of-an-object
	def get_field_values(self):
		return [(field.name, field.value_to_string(self)) for field in Brand._meta.fields]

	def __unicode__(self):
		obj_desc = u'%s' % (self.name)
		if self.origin is not None:
			obj_desc = obj_desc + u' from %s' % (self.origin)
		return obj_desc

class Flavor(models.Model):
	taste = models.CharField(max_length=128, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.taste)

class RamenManager(models.Manager):
	def ramen_count(self):
		return self.count()

class Ramen(models.Model):
	upc = models.CharField(max_length=128, blank=True, null=True)
	brand = models.ForeignKey(Brand, blank=True, null=True)
	name = models.CharField(max_length=255)
	cogs = models.IntegerField(max_length=7, blank=True, null=True)
	msrp = models.IntegerField(max_length=7, blank=True, null=True)

	# Description
	description = models.TextField(max_length=255, blank=True, null=True)
	directions = models.TextField(max_length=255, blank=True, null=True)

	# Packing
	weight = models.CharField(max_length=128, blank=True, null=True)
	dimensions = models.CharField(max_length=128, blank=True, null=True)
	packaging = models.CharField(max_length=128, blank=True, null=True)

	# Image
	image_url = models.URLField(blank=True, null=True)
	saved_image = models.ImageField(upload_to=RAMEN_FILE_PATH, blank=True)

    # Metadata
	nutrition = models.TextField(max_length=255, blank=True, null=True)
	ingredients = models.TextField(max_length=255, blank=True, null=True)
	flavors = models.ManyToManyField(Flavor, blank=True, null=True)
	ratings = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, editable=False)

	# Housekeeping
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)
	notes = models.TextField(max_length=255, blank=True, null=True)
	boxed = models.DateTimeField(blank=True, null=True, editable=False)

	objects = RamenManager()

	def get_absolute_url(self):
		return reverse('ramen_detail', kwargs={'pk': self.pk})

	#bigups http://stackoverflow.com/questions/2217478/django-templates-loop-through-and-print-all-available-properties-of-an-object
	def get_field_values(self):
		return [(field.name, field.value_to_string(self)) for field in Ramen._meta.fields]

	def __unicode__(self):
		obj_desc = u'%s' % (self.name)
		if self.brand is not None:
			obj_desc = obj_desc + u' from %s' % (self.brand.origin)
		return obj_desc

class Box(models.Model):
	"""
		Req:

		Create box for every menu object every month

		Each box has number of ramen slots defined by Box.slots from menu object

		Each box has m2m relationship to ramens in the box

		Each box cost is calculated from price of every ramen in the box

		Each monthly order has a monthly box object
	"""
	name = models.CharField(max_length=255)
	slots = models.IntegerField(max_length=2)
	cost = models.IntegerField(max_length=7, blank=True, null=True)
	notes = models.TextField(max_length=255, blank=True, null=True)
	month = models.IntegerField(max_length=2)
	year = models.IntegerField(max_length=4)
	ramens = models.ManyToManyField(Ramen, related_name='ramens')	
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)

	def get_absolute_url(self):
		return reverse('box_detail', args=[self.pk])

	#bigups http://stackoverflow.com/questions/2217478/django-templates-loop-through-and-print-all-available-properties-of-an-object
	def get_field_values(self):
		return [(field.name, field.value_to_string(self)) for field in Box._meta.fields]

	def whats_inside(self):
		return self.ramens.all()

	def total_cost(self):
		cost = 0
		for ramen in self.ramens.all():
			cost += ramen.msrp
		self.cost = cost
		return cost

	def __unicode__(self):
		return u'%s/%s %s' % (self.month, self.year, self.name)

	class Meta:
		verbose_name_plural = "boxes"

class Review(models.Model):
	ramen = models.ForeignKey(Ramen)
	text = models.TextField(max_length=255, blank=True, null=True)
	# rating # switch to https://github.com/dcramer/django-ratings
	created = models.DateTimeField(auto_now_add=True, editable=False)
	published = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return u'Review for %s' % (self.ramen.name)

#tasks create abstract base classes for housekeeping purposes
#bigups https://docs.djangoproject.com/en/dev/topics/db/models/#abstract-base-classes
# name, created

#notes
# django model _meta https://django-model-_meta-reference.readthedocs.org/en/latest/