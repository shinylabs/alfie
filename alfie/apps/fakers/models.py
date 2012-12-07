from django.db import models
from django.contrib.auth.models import User
from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Menu, Order

class FakerManager(models.Manager):
	#bigups http://stackoverflow.com/questions/4909585/interesting-takes-exactly-1-argument-2-given-python-error
	@staticmethod
	def load_csv(csvfile):
		import csv
		reader = csv.DictReader(open(csvfile))
		user_info = []
		for row in reader:
			user_info.append(row)
		return user_info

	@staticmethod
	def salt_hash(password):
		#bigups http://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
		import hashlib, uuid
		salt = uuid.uuid4().hex
		hashed_password = hashlib.sha512(password + salt).hexdigest()
		return hashed_password

	@staticmethod
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

	def make_fakers(self, user_info):
		for i in range(len(user_info)):
			f = Faker(
				username=user_info[i]['Username'],
				first_name = user_info[i]['GivenName'],
				last_name = user_info[i]['Surname'],
				email = user_info[i]['EmailAddress'],
				password = self.salt_hash(user_info[i]['Password'])
			)
			f.save()

	@staticmethod
	def create_orders():
		for i in range(2, Faker.objects.count()):
			o = Order()
			o.user = Faker.objects.get(id=i)
			o.choice = Faker.objects.get(id=i).profile.choice
			o.save()

class Faker(User):
	objects = FakerManager()

class FakeProfile(Profile):
	pass