from django.db import models
from django.contrib.auth.models import User
from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Menu, Order

from alfie.apps.fakers.csvtools import *
"""
Imports in:
	load_csv_dict(csvfile)
	load_csv(csvfile)
	write_csv(data, step=500)
"""

"""
from alfie.apps.fakers.models import Faker, Fakep
from alfie.apps.orders.models import Menu, Order
from alfie.apps.fakers.csvtools import *
users = load_csv_dict(csvfile)
Faker.objects.make_fakers(users)
"""

class FakerManager(models.Manager):
	"""
		This manager does:
			make_fakers
			make_profiles
			make_orders
	"""
	@staticmethod	#bigups http://stackoverflow.com/questions/4909585/interesting-takes-exactly-1-argument-2-given-python-error
	def salt_hash(password):
		#bigups http://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
		import hashlib, uuid
		salt = uuid.uuid4().hex
		hashed_password = hashlib.sha512(password + salt).hexdigest()
		return hashed_password

	@staticmethod
	def make_profile(f, user_info):
		import random
		p = Fakep()
		p.user = f
		p.choice = random.choice(Menu.objects.all())
		p.ship_address_1 = user_info['StreetAddress']
		p.ship_city = user_info['City']
		p.ship_state = user_info['State']
		p.ship_zip_code = user_info['ZipCode']
		p.ccnumber = user_info['CCNumber']
		p.cvv = user_info['CVV2']
		p.exp_month = user_info['CCExpires'].split('/')[0]
		p.exp_year = user_info['CCExpires'].split('/')[1]
		p.save()

	def make_fakers(self, user_info):
		successcounter = 0
		failcounter = 0
		badlist = []
		for i in range(len(user_info)):
			f = Faker(
				username=user_info[i]['Username'],
				first_name = user_info[i]['GivenName'],
				last_name = user_info[i]['Surname'],
				email = user_info[i]['EmailAddress'],
				password = self.salt_hash(user_info[i]['Password'])
			)
			try:
				f.save()
				print '\nSaved %s' % f.username
				self.objects.make_profile(f, user_info[i])
				print 'Made a profile for %s' % f.username
				successcounter+=1
			except:
				badlist.append(user_info[i]['Username'])
				print '\nSomething about %s failed :(' % f.username
				failcounter+=1
				pass
		print '\nStarted with %s users and added %s users ' % (len(user_info), successcounter)
		if failcounter > 0: print 'Failed to add %s.\nThese failed: %s' % (failcounter, badlist)

	@staticmethod
	def create_orders():
		for i in range(2, Faker.objects.count()):
			o = Order()
			o.user = Faker.objects.get(id=i)
			o.choice = Faker.objects.get(id=i).profile.choice
			o.save()

class Faker(User):
	objects = FakerManager()

class Fakep(Profile):
	ccnumber = models.CharField(max_length=16, blank=True, null=True)
	cvv =  models.CharField(max_length=3, blank=True, null=True)
	exp_month = models.CharField(max_length=2, blank=True, null=True)
	exp_year = models.CharField(max_length=4, blank=True, null=True)