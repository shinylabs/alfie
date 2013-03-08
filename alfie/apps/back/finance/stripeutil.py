"""
//SHELL CMDS

from alfie.apps.back.finance.stripeutil import *
fake_numbers()
create_token()
create_customer()
"""
import sys
import random
import datetime
now = datetime.datetime.now()

import stripe
# set api key
from django.conf import settings
stripe.api_key = settings.TEST_STRIPE_API_KEY

# p = FakeProfile.objects.get(id)
# profile = p.profile_ptr
# fakeprofile = p

def create_plans():
	"""
		Create and map Stripe plan objects out of Menu objects

		Stripe API:
			https://stripe.com/docs/api#plans

		Params:
			- name			-> Menu.name
			- amount		-> Menu.price (in cents)
			- interval		-> "month"
			- currency		-> "usd"
			- objects		-> "plan"
			- id 			-> Menu.name.lower()
			- livemode	 	-> true
	"""
	from alfie.apps.orders.models import Menu
	for menu in Menu.objects.all():
		response = stripe.Plan.create(
			id = menu.name.lower(),
			amount = menu.price,
			currency = 'usd',
			interval = 'month',
			name = menu.name
		)
		print response

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

def create_token(user, profile):
	card = {
		'number': profile.ccnumber,
		'exp_month': profile.exp_month,
		'exp_year': profile.exp_year,
		'cvc': profile.cvv,
		'name':  user.first_name + ' ' + user.last_name
	}
	print 'Made a card for %s, details: %s' % (user.username, card)

	try:
		response = stripe.Token.create(
			card = card,
		)
		print 'Made a token for %s' % user.username
		user.profile.stripe_token = response.id
		user.profile.last4 = response.card.last4
		user.profile.save()
		print 'Saved token for %s' % user.username
		return True
	except Exception,e: 
		print str(e)
		return False

def create_customer(user, profile, coupon=None):
	"""
		Takes in profile, stripe_token, create and return a stripe customer object
	"""
	if not user.profile.stripe_token:
		if create_token(user, profile.fakep):
			create_customer(user, profile)
		else: return False
	else: 
		try:
			response = stripe.Customer.create(
				card = profile.stripe_token,
				email = profile.user.email,
				plan = profile.choice.name,
				coupon = coupon
			)
			print 'Made a customer for %s' % user.username
			user.profile.stripe_cust_id = response.id
			user.profile.subscribed = now
			user.profile.save()
			print 'Saved customer for %s' % user.username
			return True
		except Exception, e:
			print str(e)
			return False

def check_overdue(profile):
	"""
		See if customer delinquent flag is true
	"""
	try:
		cu = stripe.Customer.retrieve(profile.stripe_cust_id)
		if cu['delinquent']:
			profile.overdue = True
			profile.save()
			print '%s is overdue' % profile.user.first_name
			return True
	except Exception, e:
		print str(e)
		return False

def update_sub(profile, new_choice, token=None, coupon=None, prorate=False):
	"""
		Update subscription with new choice
	"""
	try:
		cu = stripe.Customer.retrieve(profile.stripe_cust_id)
		if token:
			cu.update_subscription(token=token, coupon=coupon, prorate=prorate)
		else:
			cu.update_subscription(plan=new_choice, coupon=coupon, prorate=prorate)
		profile.subscribed = now
		profile.save()
		return True
	except Exception, e:
		print str(e)
		return False

def cancel_sub(profile):
	"""
		Cancel a subscription
	"""
	try:
		cu = stripe.Customer.retrieve(profile.stripe_cust_id)
		cu.cancel_subscription()
		profile.subscribed = None
		profile.save()
		return True
	except Exception, e:
		print str(e)
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