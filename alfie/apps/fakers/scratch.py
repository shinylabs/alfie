import random

for i in range(Faker.objects.count()):
	for j in range(len(users)):
		if Faker.objects.all()[i].username == users[j]['Username']:
			p = FakeProfile()
			p.user = Faker.objects.all()[i]
			p.choice = random.choice(Menu.objects.all())
			p.ship_address_1 = users[j]['StreetAddress']
			p.ship_city = users[j]['City']
			p.ship_state = users[j]['State']
			p.ship_zip_code = users[j]['ZipCode']
			p.ccnumber = users[j]['CCNumber']
			p.cvv = users[j]['CVV2']
			p.exp_month = users[j]['CCExpires'].split('/')[0]
			p.exp_year = users[j]['CCExpires'].split('/')[1]
			try:
				p.save()
				print 'Profile created'
			except:
				pass


for i in range(Faker.objects.count()):
	o = Order()
	o.user = Faker.objects.all()[i]
	o.choice = Faker.objects.all()[i].profile.choice
	try:
		o.save()
		print 'Order created for %s' % Faker.objects.all()[i].first_name
	except:
		pass





goodcards = ['4242424242424242', '4012888888881881', '5555555555554444', '5105105105105100', '378282246310005', '371449635398431', '6011111111111117', '6011000990139424']
badcards = ['4000000000000010', '4000000000000028', '4000000000000036', '4000000000000101', '4000000000000341', '4000000000000002', '4000000000000069', '4000000000000119']
goodlist = []
badlist = []
for i in range(1,FakeProfile.objects.count()):
	f = FakeProfile.objects.get(id=i)
	r = random.randint(0,5)
	if r is 0:
		card = random.choice(badcards)
		badlist.append(f)
	else:
		card = random.choice(goodcards)
		goodlist.append(f)
	f.ccnumber = card
	f.save()
	print 'Updated number for %s, now %s' % (f.user.first_name, f.ccnumber)

