"""
from alfie.apps.back.shipping.easyposttools import *
"""

from easypost import EasyPost, Address, Postage

"""
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

from alfie.apps.profiles.models import Profile

def verify_addr():
	pass

def set_rate(profile, price):
	try:
		profile.shipping_rate = price
		profile.save()
		return True
	except:
		return False

def check_rate(profile, box=None):
	fromzip = {"from": {"zip": "95129"}}
	tozip = {"to": {"zip": str(profile.get_addr()[-1])}}

	payload = dict(fromzip, **tozip)

	if profile.choice.id == 1:
		box = {"parcel": {"weight": 16,"height": 6,"width": 6,"length": 6}}
	if profile.choice.id == 2:
		box = {"parcel": {"weight": 48,"height": 9,"width": 9,"length": 9}}
	if profile.choice.id == 3:
		box = {"parcel": {"weight": 80,"height": 12,"width": 12,"length": 12}}

	payload.update(box)

	try:
		p = Postage.rates(**payload)
		for item in p['rates']:
			if item['service'] == 'ParcelPost':
				print '\nParcel shipping a %s oz %s from %s to %s costs $%s' % (box['parcel']['weight'], profile.choice.name, fromzip['from']['zip'], profile.get_addr()[-1], item['rate'])
				set_rate(profile, float(item['rate']))
				return (profile, float(item['rate']))
	except:
		print "Something broke :("
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

# Testing
#check_rates()