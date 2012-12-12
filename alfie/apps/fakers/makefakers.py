from alfie.apps.fakers.models import Faker, FakeProfile
from alfie.apps.orders.models import Menu, Order

from alfie.apps.fakers.csvtools import *
"""
Imports in:
	load_csv_dict(csvfile)
	load_csv(csvfile)
	write_csv(data, step=500)
"""

csvfile = 'alfie/apps/fakers/fakedata/names500.csv'
csvfile2 = 'alfie/apps/fakers/fakedata/names1000.csv'
csvfile3 = 'alfie/apps/fakers/fakedata/names1500.csv'

def salt_hash(password):
	#bigups http://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
	import hashlib, uuid
	salt = uuid.uuid4().hex
	hashed_password = hashlib.sha512(password + salt).hexdigest()
	return hashed_password

def make_profile(f, user_info):
	import random
	p = FakeProfile()
	p.user = f
	p.choice = random.choice(Menu.objects.all())
	p.ship_address_1 = user_info['StreetAddress']
	p.ship_city = user_info['City']
	p.ship_state = user_info['State']
	p.ship_zip_code = user_info['ZipCode']
	p.save()

def make_fakers(user_info):
	for i in range(len(user_info)):
		f = Faker()
		f.username = user_info[i]['Username']
		f.first_name = user_info[i]['GivenName']
		f.last_name = user_info[i]['Surname']
		f.email = user_info[i]['EmailAddress']
		f.password = salt_hash(user_info[i]['Password'])
		f.save()
		make_profile(f, user_info[i])

def make_orders():
	for i in range(2, Faker.objects.count()):
		o = Order()
		o.user = Faker.objects.get(id=i)
		o.choice = Faker.objects.get(id=i).profile.choice
		o.save()

make_fakers(load_csv(csvfile))
make_orders()