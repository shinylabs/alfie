"""
from alfie.apps.ramens.ramenutil import *

brandslist = load_csv(brandscsv)
ramensdict = load_csv_dict(ramenscsv)
make_brands(brandslist)
make_ramens(ramensdict)
set_price()
"""

import csv
import random

from django.shortcuts import get_object_or_404

from alfie.apps.back.timehelpers import *

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

def set_price():
	"""
		Randomly distribute and assign random prices
			40%/ level 1 >$0.50
			30%/ level 2 >$0.85
			20%/ level 3 >$1.00
			10%/ level 4 >$2.00
	"""
	# Get counts
	pop = Ramen.objects.all()
	pop_count = pop.count() # 510
	a = int(pop_count * .4) # 374
	b = int(pop_count * .3) # 281
	c = int(pop_count * .2) # 187
	d = int(pop_count * .1) # 93
	if a + b + c + d is not pop_count:
		remainder = pop_count - a - b - c - d
		d = d + remainder

	# Set list
	prices = ['50', '85', '100', '200']
	pop_list = []
	for p in pop:
		pop_list.append(p.id)
	random.shuffle(pop_list)
	alist = pop_list[0:a]
	blist = pop_list[a:a+b]
	clist = pop_list[a+b:a+b+c]
	dlist = pop_list[a+b+c:a+b+c+d]
	lists = []
	lists.append(alist)
	lists.append(blist)
	lists.append(clist)
	lists.append(dlist)

	# Loop through and set prices
	for i in range(len(lists)):
		for num in lists[i]:
			r = Ramen.objects.get(pk=num)
			r.msrp = prices[i]
			r.save()
	print 'Finished setting %s objects' % (pop_count)
	return True

def make_boxes():
	pass

def fill_boxes(now=now):
	if not Box.objects.all():
		Box.objects.create_boxes()
	for box in Box.objects.this_month(now):
		if not box.ramens.all():
			for slot in range(box.menu.slots):
				box.ramens.add(random.choice(Ramen.objects.all()))
				box.save()
			box.total_cost()
			box.total_weight()
			box.save()
	print 'Finished filling boxes'
	return True

def make_flavors():
	pass