"""
//SHELL CMDS

from alfie.apps.back.finance.stripetools import *
fake_numbers()
create_token()
create_customer()
"""

# time
import datetime
now = datetime.datetime.now()

# random
import random

import stripe
# set api key
from django.conf import settings
stripe.api_key = settings.TEST_STRIPE_API_KEY

# import models
from alfie.apps.fakers.models import Faker, Fakep

# p = FakeProfile.objects.get(id)
# profile = p.profile_ptr
# fakeprofile = p

def fake_numbers():
	successcount = 0
	newsuccesscount = 0
	failcount = 0
	badlist = []
	goodcards = ['4242424242424242', '4012888888881881', '5555555555554444', '5105105105105100', '378282246310005', '371449635398431', '6011111111111117', '6011000990139424']
	badcards = ['4000000000000010', '4000000000000028', '4000000000000036', '4000000000000101', '4000000000000341', '4000000000000002', '4000000000000069', '4000000000000119']
	# loop once to write out good cards
	for i in range(2,Fakep.objects.count()+2):
		try:
			f = Fakep.objects.get(pk=i)
			card = random.choice(goodcards)
			f.ccnumber = card
			f.save()
			successcount+=1
			print 'New card number for %s' % f.user.username
		except:
			badlist.append(f.user.username)
			print '\nSomething about %s failed :(' % f.user.username
			failcount+=1
			pass
	# loop twice to make bad cards every 50th profile for testing
	l = range(2,Fakep.objects.count()+1)
	for i in l[50-2::50]:
		try:
			f = Fakep.objects.get(pk=i)
			card = random.choice(badcards)
			f.ccnumber = card
			f.save()
			newsuccesscount+=1
			print '>:( bad card number for %s' % f.user.username
		except:
			badlist.append(f.user.username)
			print '\nSomething about %s failed :(' % f.user.username
			failcount+=1
			pass
	print '\nStarted with %s users and updated %s cards ' % (Fakep.objects.count(), successcount)
	print 'Made %s test cards too' % (newsuccesscount)
	if failcount > 0: print 'Failed to update %s cards.\nThese failed: %s' % (failcount, badlist)

def create_token():
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
	for i in range(1,Fakep.objects.count()+1):
		f = Fakep.objects.get(pk=i)
		if f.profile_ptr.stripe_token is None:
			card = {
				'number': f.ccnumber,
				'exp_month': f.exp_month,
				'exp_year': f.exp_year,
				'cvc': f.cvv,
				'name':  f.user.first_name + ' ' + f.user.last_name
			}
		try:
			response = stripe.Token.create(
				card = card,
			)
			print 'Made a token for %s' % f.user.username
			f.profile_ptr.stripe_token = response.id
			f.profile_ptr.last_4_digits = response.card.last4
			f.profile_ptr.save()
			successcount+=1
			print 'Saved token for %s' % f.user.username
		except:
			badlist.append(f.user.username)
			print '\nSomething about %s failed :(' % f.user.username
			failcount+=1
			pass
	print '\nStarted with %s users and created %s tokens ' % (Fakep.objects.count(), successcount)
	if failcount > 0: print 'Failed to create %s tokens.\nThese failed: %s' % (failcount, badlist)

def create_customer():
	"""
		Loop and get Fakep object
		Get payment info
		Call Stripe and create token
		Save token

		Docs: https://stripe.com/docs/api?lang=python#create_customer
	"""
	successcount = 0
	failcount = 0
	badlist = []
	for i in range(1,Fakep.objects.count()+1):
		f = Fakep.objects.get(pk=i)
		if f.profile_ptr.stripe_cust_id is None:
			token = f.profile_ptr.stripe_token
		try:
			response = stripe.Customer.create(
				card = token,
				email = f.user.email,
				plan = f.choice.name
			)
			print 'Created %s as a customer' % f.user.username
			f.profile_ptr.stripe_cust_id = response.id
			f.profile_ptr.subscribed = now
			f.profile_ptr.save()
			successcount+=1
			print 'Saved %s as a customer' % f.user.username
		except:
			badlist.append(f.user.username)
			print '\nSomething about %s failed :(' % f.user.username
			failcount+=1
			pass
	print '\nStarted with %s users and created %s customers ' % (Fakep.objects.count(), successcount)
	if failcount > 0: print 'Failed to create %s customers.\nThese failed: %s' % (failcount, badlist)

def update_customer():
	pass

def delete_customer():
	pass