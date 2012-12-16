"""
from alfie.apps.ramens.ramenutil import *
"""

import csv
from django.shortcuts import get_object_or_404
# Data objcts to work with
from alfie.apps.ramens.models import *

ramenscsv = 'alfie/apps/ramens/ramendata/ramens.csv'
brandscsv = 'alfie/apps/ramens/ramendata/brands.csv'

def load_csv_dict(csvfile):
	"""
	Returns list of data dictionaries
	"""
	reader = csv.DictReader(open(csvfile))
	datarows = []
	for row in reader:
		datarows.append(row)
	return datarows

def load_csv(csvfile):
	"""
	Returns list of header row and data rows
	"""
	reader = csv.reader(open(csvfile))
	datarows = []
	for row in reader:
		datarows.append(row)
	return datarows

def make_brands(brandslist):
	try: 
		for i in range(len(brandslist)):
			b = Brand()
			b.name = brandslist[i][0]
			b.website = brandslist[i][1]
			b.save()
		print 'Made %s brands' % (len(brandslist))
		return True
	except:
		print 'Something broke :('
		return False

def make_brand(brand):
	b = Brand()
	b.name = brand
	b.save()
	return b

def make_ramens(ramensdict):
	"""		
		- loop through list of dictionaries
		- create object
		- map dictinoary to object 
		- if brand exist then set fk
		- set brand origin
	"""
	brandlist = 0
	for ramen in ramensdict:
		newramen = Ramen()
		try:
			brand = get_object_or_404(Brand, name=ramen['Brand'])
			newramen.brand = brand
			brand.origin = ramen['Country']
			brand.save()
			print 'Linking %s' % (newramen.brand)
		except:
			brand = make_brand(ramen['Brand'])
			newramen.brand = brand
			brand.origin = ramen['Country']
			brand.save()
			print 'Saving %s' % (newramen.brand)
			brandlist += 1
		newramen.name = ramen['Variety']
		newramen.packaging = ramen['Style']
		newramen.ratings = ramen['Stars']
		newramen.save()
		print 'Saved %s\n' % (newramen.name)
	print 'Success, made %s ramens out of a list of %s' % (Ramen.objects.count(), len(ramensdict))
	print 'Made %s brands' % (brandlist)
	return True

def make_boxes():
	pass

def make_flavors():
	pass

brandslist = load_csv(brandscsv)
ramensdict = load_csv_dict(ramenscsv)