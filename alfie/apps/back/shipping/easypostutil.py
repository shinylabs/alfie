"""
//SHELL CMDS

from alfie.apps.back.shipping.easypostutil import *
"""

from easypost import EasyPost, Address, Postage
"""
Imports in:
	class EasyPost(object):
	  def api_url(cls, ttype='', action=''):
	  def post(cls, url, params):
	  def encode_dict(cls, stk, key, dictvalue):
	  def _encode_inner(cls, d):
	  def _utf8(cls, value):
	  def encode(cls, d):

	class Address(object):
	  def verify(cls, **address):

	class Postage(object):
	  def rates(cls, **data):
	  def compare(cls, **data):
	  def buy(cls, **data):
	  def get(cls, filename):
	  def list(cls):
"""

import sys

from alfie.apps.profiles.models import Profile

def verify_addr(profile):
	payload = {
		'street1': profile.ship_address_1,
		'street2': profile.ship_address_2,
		'city': profile.ship_city,
		'state': profile.ship_state,
		'zip': profile.ship_zip_code
	}
	print 'Verifying %s' % payload
	try:
		response = Address.verify(**payload)
		print >>sys.stderr, response
		if response['error']:
			return False
		else:
			return True
	except:
		print >>sys.stderr, 'Something broke :('
		return False


def set_rate(profile, price):
	try:
		profile.shipping_rate = price * 100
		profile.save()
		return True
	except:
		return False

def check_rate(profile, box=None):
	fromzip = {"from": {"zip": "95129"}}
	tozip = {"to": {"zip": str(profile.get_addr()['zip'])}}

	payload = dict(fromzip, **tozip)

	if profile.choice.id == 1:
		box = {"parcel": {"weight": 16,"height": 6,"width": 6,"length": 6}}
	if profile.choice.id == 2:
		box = {"parcel": {"weight": 48,"height": 9,"width": 9,"length": 9}}
	if profile.choice.id == 3:
		box = {"parcel": {"weight": 80,"height": 12,"width": 12,"length": 12}}

	payload.update(box)
	print >>sys.stderr, payload

	try:
		response = Postage.rates(**payload)
		print >>sys.stderr, response
		for item in response['rates']:
			if item['service'] == 'ParcelSelect':
				print >>sys.stderr, '\nParcel shipping a %s oz %s from %s to %s costs $%s' % (box['parcel']['weight'], profile.choice.name, fromzip['from']['zip'], profile.get_addr()['zip'], item['rate'])
				set_rate(profile, float(item['rate']))
				return float(item['rate'])
	except:
		print >>sys.stderr, "Check rate failed :("
		pass

def check_rates():
	tinypricelist = []
	bigpricelist = []
	sumopricelist = []
	for i in range(Profile.objects.count()):
		k, v = check_rate(Profile.objects.all()[i])
		if k.choice.name == 'tinybox':
			tinypricelist.append(v)
		if k.choice.name == 'bigbox':
			bigpricelist.append(v)
		if k.choice.name == 'sumobox':
			sumopricelist.append(v)
	#bigups http://stackoverflow.com/questions/7716331/calculating-arithmetic-mean-average-in-python
	print '\nAveraged costs for %s items total.' % (len(tinypricelist)+len(bigpricelist)+len(sumopricelist))

	avg_ship_price = float(sum(tinypricelist))/len(tinypricelist) if len(tinypricelist) > 0 else float('nan')
	print 'Average cost for tinybox is $%.2f' % (avg_ship_price)
	avg_ship_price = float(sum(bigpricelist))/len(bigpricelist) if len(bigpricelist) > 0 else float('nan')
	print 'Average cost for bigbox is $%.2f' % (avg_ship_price)
	avg_ship_price = float(sum(sumopricelist))/len(sumopricelist) if len(sumopricelist) > 0 else float('nan')
	print 'Average cost for sumobox is $%.2f' % (avg_ship_price)

# Testing calls
#check_rates()