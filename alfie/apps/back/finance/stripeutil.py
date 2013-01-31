"""
//SHELL CMDS

from alfie.apps.back.finance.stripeutil import *
fake_numbers()
create_token()
create_customer()
"""
import sys

# time
import datetime
now = datetime.datetime.now()

# random
import random

import stripe
# set api key
from django.conf import settings
stripe.api_key = settings.TEST_STRIPE_API_KEY

# p = FakeProfile.objects.get(id)
# profile = p.profile_ptr
# fakeprofile = p

def fake_numbers():
	"""
		Old fake numbers generator
	"""
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

def create_customer(profile, stripe_token, **kwargs):
	"""
		Takes in profile, stripe_token, create and return a stripe customer object
	"""
	try:
		response = stripe.Customer.create(
			card = stripe_token,
			email = profile.user.email,
			plan = profile.choice.name,
			coupon = kwargs['coupon'],
		)
		return response.id
	except:
		pass

def update_customer(profile, **kwargs):
	"""
		Updates customer payment info
	"""
	cu = stripe.Customer.retrieve(profile.stripe_cust_id)
	if stripe_token:
		cu.card = stripe_token
		cu.save()
		profile.stripe_token = stripe_token
		profile.save()
	return True

def delete_customer(profile):
	"""
		Deletes a customer
	"""
	cu = stripe.Customer.retrieve(profile.stripe_cust_id)
	try:
		cu.cancel_subscription()
	except:
		pass

def update_subscription(profile, choice, prorate="False"):
	"""
		Retrieve customer id then update parameters
	"""
	cu = stripe.Customer.retrieve(profile.stripe_cust_id)
	try:
		cu.update_subscription(plan=choice, prorate=prorate)
		return True
	except:
		pass
		return False

def coupon_list():
	return stripe.Coupon.all()

def create_coupon(name, percent_off=0, max_redemptions=0):
	response = stripe.Coupon.create(
			id=name,
			duration='once',
			percent_off=percent_off,
			max_redemptions=max_redemptions
		)
	return response