# time
import datetime
now = datetime.datetime.now()
import random
import stripe

from alfie.apps.fakers.models import Faker, FakeProfile

from django.conf import settings
stripe.api_key = settings.TEST_STRIPE_API_KEY
livemode_flag = 'true'

def create_token():
	pass

# p = FakeProfile.objects.get(id)
# profile = p.profile_ptr
# fakeprofile = p
badlist = []
def create_customer(profile, fakeprofile=None, token=None, coupon=None):
	if token is None and fakeprofile is not None:
		card = {
			'number': fakeprofile.ccnumber,
			'exp_month': fakeprofile.exp_month,
			'exp_year': fakeprofile.exp_year,
			'cvc': fakeprofile.cvv,
			'name':  fakeprofile.user.first_name + ' ' + fakeprofile.user.last_name
		}
	else:
		card = token

	try:
		response = stripe.Customer.create(
			card = card,
			coupon = coupon,
			email = profile.user.email,
			plan = profile.choice.name
		)

		profile.subscribed = now
		profile.last_payment_attempt = now
		profile.stripe_cust_id = response.id
		profile.save()

		if fakeprofile is not None:
			fakeprofile.save()
		
		print 'Success! %s' % response.id
	except:
		print 'Failed :('
		badlist.append(fakeprofile)
		pass

def update_customer():
	pass

def delete_customer():
	pass