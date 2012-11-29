from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Where to store all the images in devmode
MEDIA_PATH = 'alfie/media/'
RAMEN_FILE_PATH = 'img/ramen/'

class Manufacturer(models.Model):
	name = models.CharField(max_length=128, blank=True, null=True)
	address = models.TextField(max_length=255, blank=True, null=True)
	website = models.URLField(max_length=255, blank=True, null=True)
	origin = models.CharField(max_length=128, blank=True, null=True)

	def __unicode__(self):
		return u'%s in %s' % (self.name, self.origin)

class Flavor(models.Model):
	taste = models.CharField(max_length=128, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.taste)

class Ramen(models.Model):
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
	notes = models.TextField(max_length=255, blank=True, null=True)
	upc = models.CharField(max_length=128, blank=True, null=True)
	mfg = models.ForeignKey(Manufacturer, blank=True, null=True)
	weight = models.CharField(max_length=128, blank=True, null=True)
	dimensions = models.CharField(max_length=128, blank=True, null=True)
	description = models.TextField(max_length=255, blank=True, null=True)
	directions = models.TextField(max_length=255, blank=True, null=True)
	nutrition = models.TextField(max_length=255, blank=True, null=True)
	ingredients = models.TextField(max_length=255, blank=True, null=True)
	flavors = models.ManyToManyField(Flavor, blank=True, null=True)
	# Image data
	image_url = models.URLField(blank=True, null=True)
	saved_image = models.ImageField(upload_to=RAMEN_FILE_PATH, blank=True)
    # Backoffice
	ratings = models.IntegerField(blank=True, null=True)
	# Housekeeping
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)

	def __unicode__(self):
		obj_desc = u'%s' % (self.name)
		if self.mfg.origin is not None:
			obj_desc = obj_desc + u' from %s' % (self.mfg.origin)
		return obj_desc

class Box(models.Model):
	ramens = models.ManyToManyField(Ramen, through='Membership')
	month = models.CharField(max_length=2)
	year = models.CharField(max_length=4)
	created = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)

	def __unicode__(self):
		return u'%s/%s Box' % (self.month, self.year)

	class Meta:
		verbose_name_plural = "boxes"

class Membership(models.Model):
	ramen = models.ForeignKey(Ramen)
	box = models.ForeignKey(Box)

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