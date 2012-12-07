from alfie.apps.fakers.models import Faker, FakeProfile
from alfie.apps.orders.models import Menu, Order

csvfile = 'alfie/apps/fakers/names50.csv'

def LoadCsv(csvfile):
	import csv
	reader = csv.DictReader(open(csvfile))
	user_info = []
	for row in reader:
		userDicts.append(row)
	return user_info

def SaltHash(password):
	#bigups http://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
	import hashlib, uuid
	salt = uuid.uuid4().hex
	hashed_password = hashlib.sha512(password + salt).hexdigest()
	return hashed_password

def makeProfile(f, user_info):
	import random
	p = FakeProfile()
	p.user = f
	p.choice = random.choice(Menu.objects.all())
	p.ship_address_1 = user_info['StreetAddress']
	p.ship_city = user_info['City']
	p.ship_state = user_info['State']
	p.ship_zip_code = user_info['ZipCode']
	p.save()

def makeFakers(user_info):
	for i in range(len(user_info)):
		f = Faker()
		f.username = user_info[i]['Username']
		f.first_name = user_info[i]['GivenName']
		f.last_name = user_info[i]['Surname']
		f.email = user_info[i]['EmailAddress']
		f.password = SaltHash(user_info[i]['Password'])
		f.save()
		makeProfile(f, user_info[i])

def makeOrders():
	for i in range(2, Faker.objects.count()):
		o = Order()
		o.user = Faker.objects.get(id=i)
		o.choice = Faker.objects.get(id=i).profile.choice
		o.save()

makeFakers(LoadCsv(csvfile))
makeOrders()