"""
//SHELL CMDS

from alfie.apps.back.shipping.easypostutil import *
"""

# import models
from alfie.apps.profiles.models import *

import sys # to print

# import app
#from easypost import EasyPost, Address, Postage

# USPS Zones and Transit
# http://www.survivalsuppliers.com/images/zone_map.gif
# N-CA zip codes http://info.kaiserpermanente.org/steps/zipcodes_nocal.html
# S-CA zip codes http://info.kaiserpermanente.org/steps/zipcodes_socal.html
# W-NV zip codes http://www.mongabay.com/igapo/zip_codes/counties/alpha/Nevada%20County-California1.html
# W-PA zip codes
# E-PA zip codes

zone0 = ['CA', 'NV'] # 1 day
zone1 = ['CA', 'WA', 'OR', 'ID', 'NV', 'UT'] # 2 days
zone2 = ['MT', 'WY', 'CO', 'AZ', 'NM'] # 3 days
zone3 = ['ND', 'NE', 'KS', 'OK', 'TX', 'IA', 'MO', 'AR', 'WI', 'IL', 'IN', 'MI'] # 4 days
zone4 = ['SD', 'MN', 'OH', 'KY', 'TN', 'MS', 'LA', 'WV', 'PA', 'NY'] # 5 days
zone5 = ['ME', 'VT', 'NH', 'MA', 'CT', 'RI', 'NJ', 'MD', 'DE', 'DC', 'VA', 'NC', 'SC', 'GA', 'AL', 'FL'] # 6 days
zone6 = ['AL', 'HI'] # 7 days

zones = [{'zone': '0', 'states': zone0, 'transit': '1 day'}, 
		 {'zone': '1', 'states': zone1, 'transit': '2 days'},
		 {'zone': '2', 'states': zone2, 'transit': '3 days'},
		 {'zone': '3', 'states': zone3, 'transit': '4 days'},
		 {'zone': '4', 'states': zone4, 'transit': '5 days'},
		 {'zone': '5', 'states': zone5, 'transit': '6 days'},
		 {'zone': '6', 'states': zone6, 'transit': '7 days'}]

def verify_zone(state, zones):
	"""
		Inputs state to check and zones dictionary
		Loop through zones list and find state
		Returns zone list
	"""
	for region in zones:
		if state in region['states']:
			return region['zone']
			break

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

def buy_postage():
	"""
		Docs: https://www.geteasypost.com/docs/python#postage-buying

		Inputs in order
		Calls check_rate to verify rate
		Buys postage
		Saves rate, label_img, label_url, tracking_code
		Returns success message
	"""
	pass