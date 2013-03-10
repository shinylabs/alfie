from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

# time helpers
from alfie.apps.back.timehelpers import *
"""
	Imports in:
	datetime
	add_months()
	subtract_months()
"""

# Import EasyPost
import easypost.easypost
from django.conf import settings
easypost.easypost.api_key = settings.TEST_EASYPOST_API_KEY

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
	description = models.TextField(max_length=255, blank=True, null=True) # 100 words
	directions = models.TextField(max_length=255, blank=True, null=True) # list

	# Packing
	weight = models.CharField(max_length=128, blank=True, null=True) # weight in grams
	dimensions = models.CharField(max_length=128, blank=True, null=True) # x by y by z in mm
	packaging = models.CharField(max_length=128, blank=True, null=True) # packaging type: bowl, packs, cup
	boxing = models.CharField(max_length=128, blank=True, null=True) # how many units in a box: 1/12

	# Image
	image_url = models.URLField(blank=True, null=True)
	saved_image = models.ImageField(upload_to=RAMEN_FILE_PATH, blank=True)

    # Metadata
	nutrition = models.TextField(max_length=255, blank=True, null=True) # nutrition facts, serving size, calories, fat calories
	ingredients = models.TextField(max_length=255, blank=True, null=True) # list
	flavors = models.ManyToManyField(Flavor, blank=True, null=True) # list
	ratings = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, editable=False)

	# Housekeeping
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)
	shipped = models.DateTimeField(blank=True, null=True, editable=False)
	notes = models.TextField(max_length=255, blank=True, null=True)

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
		obj_desc = obj_desc + u' [%s]' % (self.id)
		return obj_desc

#tasks move Box into its own app
class BoxManager(models.Manager):
	def create_empty_box(self, menu_option, when=now):
		box = self.create(
			month=when.month, 
			year=when.year,
			menu=menu_option
			)
		box.save()
		return True

	def create_boxes(self):
		# import Menu
		from alfie.apps.orders.models import Menu
		# check latest box
		from django.db.models import Max
		max_month = Box.objects.all().aggregate(Max('month'))['month__max']
		if not max_month:
			push = now
		else: 
			push = add_months(now, max_month-now.month+1)
		# loop through menu and create boxes
		for option in Menu.objects.all():
			self.create_empty_box(option, push)

	def this_month(self, when=now):
		return self.filter(year=when.year).filter(month=when.month)

class Box(models.Model):
	"""
		Create box for every menu object every month

		Each box has number of slots from Menu.objects.slots

		Each box has m2m relationship to ramens in the box

		Each box cost is calculated from price of every ramen in the box

		Each monthly order has a monthly box object
	"""
	month = models.IntegerField(max_length=2)
	year = models.IntegerField(max_length=4)
	menu = models.ForeignKey('orders.Menu', related_name='boxes', blank=True, null=True)
	ramens = models.ManyToManyField(Ramen, related_name='ramens', blank=True, null=True)
	cost = models.IntegerField(max_length=7, blank=True, null=True)
	weight = models.IntegerField(max_length=7, blank=True, null=True)
	profit = models.IntegerField(max_length=7, blank=True, null=True)

	# Housekeeping
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, editable=False)
	notes = models.TextField(max_length=255, blank=True, null=True)

	objects = BoxManager()

	def get_absolute_url(self):
		return reverse('box_detail', args=[self.pk])

	#bigups http://stackoverflow.com/questions/2217478/django-templates-loop-through-and-print-all-available-properties-of-an-object
	def get_field_values(self):
		return [(field.name, field.value_to_string(self)) for field in Box._meta.fields]

	def whats_inside(self):
		return self.ramens.all()

	def total_weight(self):
		weight = 0
		for ramen in self.ramens.all():
			weight += int(0 if ramen.weight is None else ramen.weight)
		self.weight = weight
		self.save()
		return "Box weighs %sg" % (weight)

	def total_cost(self):
		cost = 0
		for ramen in self.ramens.all():
			cost += int(0 if ramen.msrp is None else ramen.msrp)
		self.cost = cost
		self.save()
		return "Box costs $%.2f" % (float(cost) / 100)

	def create_package(self):
		#todo call self.total_weight() and convert to oz
		if self.menu.slots is 4:
			package = {"height": 7, "width": 7, "length": 7, "weight": 16}
		if self.menu.slots is 8:
			package = {"height": 10, "width": 10, "length": 10, "weight": 48}
		if self.menu.slots is 12:
			package = {"height": 13, "width": 13, "length": 13, "weight": 80}

		return easypost.easypost.Package(**package)

	def __unicode__(self):
		if not self.ramens.all():
			status = 'empty'
		else:
			status = 'full'
		return u'%s - %s/%s - %s with %s slots - %s' % (self.id, self.month, self.year, self.menu.name.capitalize(), self.menu.slots, status.upper())

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