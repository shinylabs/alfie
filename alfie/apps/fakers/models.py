"""
//SHELL CMDS

from alfie.apps.fakers.models import *
from alfie.apps.orders.models import Order, Menu
users = load_csv_dict(csvfile)
Faker.objects.create_fakers(users)
Faker.objects.create_bad_fakers(50)
Faker.objects.create_fake_orders()
Faker.objects.create_fake_tokens()
Faker.objects.create_fake_customers()
Faker.objects.verify_fake_addr()
Faker.objects.rate_fake_addr()
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

# util
from alfie.apps.fakers.csvutil import *
"""
	Imports in:
	load_csv_dict(csvfile)
	load_csv(csvfile)
	write_csv(data, step=500)
"""

import stripe
# set api key
from django.conf import settings
stripe.api_key = settings.TEST_STRIPE_API_KEY

from alfie.apps.back.shipping.easypost import *
from alfie.apps.back.shipping.easypostutil import verify_addr, check_rate

class FakerManager(models.Manager):
	"""
		This object manager does:
			salt/hash passwords
			create fakers
			create fake profiles
			create fake orders
			verify fake address
			rate fake address
	"""
	@staticmethod	#bigups http://stackoverflow.com/questions/4909585/interesting-takes-exactly-1-argument-2-given-python-error
	def salt_hash(password):
		#bigups http://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
		import hashlib, uuid
		salt = uuid.uuid4().hex
		hashed_password = hashlib.sha512(password + salt).hexdigest()
		return hashed_password

	@staticmethod
	def create_profile(f, user_info):
		import random
		# cc from csv don't pass stripe security test
		goodcards = ['4242424242424242', '4012888888881881', '5555555555554444', '5105105105105100', '378282246310005', '371449635398431', '6011111111111117', '6011000990139424']

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

		p.ccnumber = random.choice(goodcards) # user_info['CCNumber']
		p.cvv = user_info['CVV2']
		p.exp_month = user_info['CCExpires'].split('/')[0]
		p.exp_year = user_info['CCExpires'].split('/')[1]
		p.save()

	def create_fakers(self, user_info):
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
				self.create_profile(f, user_info[i])
				print 'Made a profile for %s' % f.username
				successcount+=1
			except:
				badlist.append(user_info[i]['Username'])
				print '\nSomething about %s failed :(' % f.username
				failcount+=1
				pass
		print '\nStarted with %s users and added %s users ' % (len(user_info), successcount)
		stat = Stat(key='fakers', value=successcount).save()
		if failcount > 0: print 'Failed to add %s.\nThese failed: %s' % (failcount, badlist)

	def create_bad_fakers(self, num=1):
		"""
			Randomly choose num of fakers and update ccnumber to be bad
		"""
		import random

		# these fail stripe security test
		badcards = ['4000000000000010', '4000000000000028', '4000000000000036', '4000000000000101', '4000000000000341', '4000000000000002', '4000000000000069', '4000000000000119']

		successcount = 0
		failcount = 0
		badlist = []
		for i in range(num):
			f = random.choice(Faker.objects.all())
			try:
				f.profile.ccnumber = random.choice(badcards)
				f.save()
				print '\nUpdated credit card for %s' % f.first_name
				successcount+=1
				stat = Stat(key='bad faker', value=f.id).save()
			except:
				badlist.append(f.username)
				print '\nSomething about %s failed :(' % f.first_name
				failcount+=1
				pass
		print '\nCreated %s bad fakers' % (successcount)
		if failcount > 0: print 'Failed to create %s bad fakers.\nThese failed: %s' % (failcount, badlist)

	def create_fake_orders(self, when=now):
		successcount = 0
		failcount = 0
		badlist = []
		for i in range(2, self.count()+2): # +2 for admin profiles
			f = self.get(pk=i)
			o = Order()
			o.user = f
			o.choice = f.profile.choice
			try:
				o.save()
				# hack around auto_now_add
				o.created = when
				o.save()
				print '\nCreated an order for %s' % f.username
				successcount+=1
			except:
				badlist.append(f.username)
				print '\nSomething about %s failed :(' % f.username
				failcount+=1
				pass
		print '\nStarted with %s users and added %s orders in %s/%s' % (self.count(), successcount, when.month, when.year)
		stat = Stat(key='orders', value=successcount).save()
		if failcount > 0: print 'Failed to add %s.\nThese failed: %s' % (failcount, badlist)

	def create_fake_tokens(self):
		"""
			Loop and get Fakep object
			Get payment info
			Call Stripe and create token
			Save token

			Docs: https://stripe.com/docs/api?lang=python#tokens
		"""
		successcount = 0
		failcount = 0
		badlist = []
		for i in range(2,self.count()+2):
			f = self.get(pk=i)
			p = Fakep.objects.get(pk=f.profile.id)
			if f.profile.stripe_token is None or f.profile.stripe_token == '':
				card = {
					'number': p.ccnumber,
					'exp_month': p.exp_month,
					'exp_year': p.exp_year,
					'cvc': p.cvv,
					'name':  f.first_name + ' ' + f.last_name
				}
				print 'Made a card for %s, details: %s' % (f.username, card)

				try:
					response = stripe.Token.create(
						card = card,
					)
					print 'Made a token for %s' % f.username
					f.profile.stripe_token = response.id
					f.profile.last_4_digits = response.card.last4
					f.profile.save()
					successcount+=1
					print 'Saved token for %s\n' % f.username

				except:
					badlist.append(f.id)
					print '\nSomething about %s failed :(' % f.username
					failcount+=1
					pass

		print '\nStarted with %s users and created %s tokens ' % (self.count(), successcount)
		if failcount > 0: 
			badfakers = []
			for i in range(Stat.objects.count()):
				if Stat.objects.all()[i].key == 'bad faker':
					badfakers.append(Stat.objects.all()[i].value)
			matches = set(badfakers) & set(badlist)
			if matches is len(badfakers):
				print 'Failed to create %s tokens but %s were expected to fail' % (failcount, len(badfakers))
			else:
				print 'Failed to create %s tokens and even though %s were expected to fail %s did not match up.' % (failcount, len(badfakers), len(matches))

	def create_fake_customers(self):
		"""
			If not customer, create a stripe customer id
		"""
		successcount = 0
		failcount = 0
		badlist = []
		for i in range(2,self.count()+2):
			f = self.get(pk=i)
			if f.profile.stripe_cust_id is None or f.profile.stripe_cust_id == '':
				token = f.profile.stripe_token
				try:
					response = stripe.Customer.create(
						card = token,
						email = f.email,
						plan = f.profile.choice.name
					)
					print 'Created %s as a customer' % f.username
					f.profile.stripe_cust_id = response.id
					f.profile.subscribed = now
					f.profile.save()
					successcount+=1
					print 'Saved %s as a customer\n' % f.username
				except stripe.CardError, e:
					body = e.json_body
					err  = body['error']
					print '\nSomething about %s failed :(' % f.username
					print "Status is: #{e.http_status}\n"
					print "Type is: #{err['type']}\n"
					print "Code is: #{err['code']}\n"
					# param is '' in this case
					print "Param is: #{err['param']}\n"
  					print "Message is: #{err['message']}\n"

					badlist.append(f.username)
					failcount+=1
					pass
		print '\nStarted with %s users and created %s customers ' % (self.count(), successcount)
		if failcount > 0: print 'Failed to create %s customers.\nThese failed: %s' % (failcount, badlist)

	def verify_fake_addr(self):
		"""
			If not verified, check address
		"""
		successcount = 0
		failcount = 0
		badlist = []
		for i in range(2,self.count()+2):
			f = self.get(pk=i)
			if f.profile.address_verified is False:
				try:
					f.profile.address_verified = verify_addr(f.profile)
					f.profile.save()
					successcount+=1
					print 'Verified address for %s' % f.username
				except:
					badlist.append(f.username)
					print '\nSomething about %s failed :(' % f.username
					failcount+=1
					pass
		print '\nStarted with %s users and verified %s customers ' % (self.count(), successcount)
		if failcount > 0: print 'Failed to verify %s customers.\nThese failed: %s' % (failcount, badlist)

	def rate_fake_addr(self):
		"""
			If no rate, check and save rate
		"""
		successcount = 0
		failcount = 0
		badlist = []
		for i in range(2,self.count()+2):
			f = self.get(pk=i)
			try:
				f.profile.shipping_rate = check_rate(f.profile)
				f.profile.save()
				successcount+=1
				print 'Costs $%s to ship to %s in %s' % (f.profile.shipping_rate, f.username, f.profile.ship_state)
			except:
				badlist.append(f.username)
				print '\nSomething about %s failed :(' % f.username
				failcount+=1
				pass
		print '\nStarted with %s users and verified %s customers ' % (self.count(), successcount)
		if failcount > 0: print 'Failed to verify %s customers.\nThese failed: %s' % (failcount, badlist)

	def delete_fake_orders(self, when=now):
		"""
			Loop through and delete fake orders, filter based on datetime
		"""
		successcount = 0
		failcount = 0
		badlist = []
		for i in range(2, self.count()+2): # +2 for admin profiles
			f = self.get(pk=i)
			o = Order()
			o.user = f
			o.choice = f.profile.choice
			try:
				o.save()
				# hack around auto_now_add
				o.created = when
				o.save()
				print '\nCreated an order for %s' % f.username
				successcount+=1
			except:
				badlist.append(f.username)
				print '\nSomething about %s failed :(' % f.username
				failcount+=1
				pass
		print '\nStarted with %s users and added %s orders in %s/%s' % (self.count(), successcount, when.month, when.year)
		stat = Stat(key='orders', value=successcount).save()
		if failcount > 0: print 'Failed to add %s.\nThese failed: %s' % (failcount, badlist)


	def delete_fakers(self):
		"""
			Loop through and delete faker and fakep
		"""
		pass

class Faker(User):
	objects = FakerManager()

class Fakep(Profile):
	ccnumber = models.CharField(max_length=16, blank=True, null=True)
	cvv =  models.CharField(max_length=3, blank=True, null=True)
	exp_month = models.CharField(max_length=2, blank=True, null=True)
	exp_year = models.CharField(max_length=4, blank=True, null=True)

#bigups http://stackoverflow.com/questions/8141460/saving-results-of-django-model-manager-to-database
class Stat(models.Model):
	"""
	Usage:
		stat = Stat(name='some_name', value=count).save()
	"""
	key = models.CharField(max_length=128, blank=True, null=True)
	value = models.CharField(max_length=128, blank=True, null=True)