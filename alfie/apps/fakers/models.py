"""
from alfie.apps.fakers.models import Faker, Fakep
from alfie.apps.fakers.csvtools import *
users = load_csv_dict(csvfile)
Faker.objects.make_fakers(users)
Faker.objects.create_orders()
"""

# time
import datetime
import calendar
now = datetime.datetime.now()

#bigups http://stackoverflow.com/questions/4130922/how-to-increment-datetime-month-in-python
def add_months(sourcedate, months):
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month / 12
	month = month % 12 + 1
	day = min(sourcedate.day, calendar.monthrange(year,month)[1])
	return datetime.date(year, month, day)

def subtract_months(sourcedate, months):
	month = sourcedate.month - 1 - months
	year = sourcedate.year + month / 12
	month = month % 12 + 1
	day = min(sourcedate.day, calendar.monthrange(year,month)[1])
	return datetime.date(year, month, day)

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

		p.cutest = random.choice(p.CUTE_CHOICES)[0]
		p.spicy = random.choice(p.SPICY_LEVEL_CHOICES)[0]
		p.allergy = random.choice(p.ALLERGY_TYPE_CHOICES)[0]

		p.ccnumber = user_info['CCNumber']
		p.cvv = user_info['CVV2']
		p.exp_month = user_info['CCExpires'].split('/')[0]
		p.exp_year = user_info['CCExpires'].split('/')[1]

		p.save()

	def make_fakers(self, user_info):
		successcount = 0
		failcount = 0
		badlist = []
		for i in range(len(user_info)):
			f = Faker(
				username=user_info[i]['Username'],
				first_name = user_info[i]['GivenName'],
				last_name = user_info[i]['Surname'],
				email = user_info[i]['EmailAddress'],
				#password = self.salt_hash(user_info[i]['Password'])
				password = user_info[i]['Password']
			)
			try:
				f.save()
				print '\nSaved %s' % f.username
				self.make_profile(f, user_info[i])
				print 'Made a profile for %s' % f.username
				successcount+=1
			except:
				badlist.append(user_info[i]['Username'])
				print '\nSomething about %s failed :(' % f.username
				failcount+=1
				pass
		print '\nStarted with %s users and added %s users ' % (len(user_info), successcount)
		if failcount > 0: print 'Failed to add %s.\nThese failed: %s' % (failcount, badlist)

	def create_orders(self, when=now):
		successcount = 0
		failcount = 0
		badlist = []
		for i in range(2, self.count()+2): # +2 for admin profiles
			f = self.get(pk=i)
			o = Order()
			o.user = f
			o.choice = f.profile.choice
			o.created = when
			try:
				o.save()
				print '\nCreated an order for %s' % f.username
				successcount+=1
			except:
				badlist.append(f.username)
				print '\nSomething about %s failed :(' % f.username
				failcount+=1
				pass
		print '\nStarted with %s users and added %s users ' % (self.count(), successcount)
		if failcount > 0: print 'Failed to add %s.\nThese failed: %s' % (failcount, badlist)

	def charge_orders(self):
		print self.get(id=10)

class Faker(User):
	objects = FakerManager()

class Fakep(Profile):
	ccnumber = models.CharField(max_length=16, blank=True, null=True)
	cvv =  models.CharField(max_length=3, blank=True, null=True)
	exp_month = models.CharField(max_length=2, blank=True, null=True)
	exp_year = models.CharField(max_length=4, blank=True, null=True)