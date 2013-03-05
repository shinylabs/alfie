"""
from alfie.apps.fakers.fakersutil import *
"""
import random

from alfie.apps.fakers.models import Faker, Fakep
from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Menu, Order
from alfie.apps.ramens.models import Ramen

from alfie.apps.fakers.csvutil import *
"""
Imports in: 
	load_csv_dict(csvfile)
	load_csv(csvfile)
	write_csv(data, step=500)
"""

csvfile = 'alfie/apps/fakers/fakedata/names.csv'

def salt_hash(password):
	#bigups http://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
	import hashlib, uuid
	salt = uuid.uuid4().hex
	hashed_password = hashlib.sha512(password + salt).hexdigest()
	return hashed_password

def make_profile(f, user_info):
	p = Fakep()
	p.user = f
	p.choice = random.choice(Menu.objects.all())
	p.ship_address_1 = user_info['StreetAddress']
	p.ship_city = user_info['City']
	p.ship_state = user_info['State']
	p.ship_zip_code = user_info['ZipCode']
	p.save()

def make_fakers(user_info):
	fakers_count = Faker.objects.count()

	if fakers_count is 0:
		print 'There are no fakers'
		make_count = raw_input('How many fakers do you want to make? ')
		print 'Making', make_count

		"""
		for i in range(len(user_info)):
			f = Faker()
			f.username = user_info[i]['Username']
			f.first_name = user_info[i]['GivenName']
			f.last_name = user_info[i]['Surname']
			f.email = user_info[i]['EmailAddress']
			f.password = salt_hash(user_info[i]['Password'])
			f.save()
			make_profile(f, user_info[i])
		"""
	else:
		confirm_making = raw_input('There are ' + str(fakers_count) + ' fakers already. Do you want to make more? (y/n) ')
		if confirm_making is 'y':
			print confirm_making
		else:
			print confirm_making

def make_orders():
	for i in range(2, Faker.objects.count()):
		o = Order()
		o.user = Faker.objects.get(id=i)
		o.choice = Faker.objects.get(id=i).profile.choice
		o.save()

def make_box():
	"""
	"""
	pass

def pick_menu():
	"""
		Randomly distribute and pick menu choices for the population
			50%/ plan A
			45%/ plan B
			5%/ plan C

		get count of population
		get count of distribution
		loop through pop count
		assign menu choice
		increment dist count, stop if met
	"""
	# Get counts
	pop_count = Profile.objects.count() # 510
	a = int(pop_count * .5) # 306
	b = int(pop_count * .45) # 153
	c = int(pop_count * .5) # 51

	# Set list
	pop_list = list(range(1, pop_count+1))
	random.shuffle(pop_list)
	alist = pop_list[0:a]
	blist = pop_list[a:a+b]
	clist = pop_list[a+b:a+b+c]
	lists = []
	lists.append(alist)
	lists.append(blist)
	lists.append(clist)

	# Loop through and set profile objects
	for i in range(len(lists)):
		for num in lists[i]:
			p = Profile.objects.get(pk=num)
			m = Menu.objects.get(pk=i+1)
			p.choice = m
			p.save()
	print 'Finished setting %s objects' % (Profile.objects.count())

def set_price():
	"""
		Randomly distribute and assign random prices
			40%/ level 1 >$0.50
			30%/ level 2 >$0.85
			20%/ level 3 >$1.00
			10%/ level 4 >$2.00
	"""
	# Get counts
	pop_count = Ramen.objects.count() # 510
	a = int(pop_count * .4) # 374
	b = int(pop_count * .3) # 281
	c = int(pop_count * .2) # 187
	d = int(pop_count * .1) # 93

	# Set list
	price_list = ['0.50', '0.85', '1.00', '2.00']
	pop_list = list(range(1, pop_count+1))
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

	# Loop through and set profile objects
	for i in range(len(lists)):
		for num in lists[i]:
			r = Ramen.objects.get(pk=num)
			r.msrp = price_list[i]
			r.save()
	print 'Finished setting %s objects' % (Ramen.objects.count())