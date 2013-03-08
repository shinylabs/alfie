import random

from alfie.apps.profiles.models import Profile
from alfie.apps.orders.models import Menu

def salt_hash(password):
	#bigups http://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
	import hashlib, uuid
	salt = uuid.uuid4().hex
	hashed_password = hashlib.sha512(password + salt).hexdigest()
	return hashed_password

def pick_menu(a_odds=.35, b_odds=.5, c_odds=.15):
	"""
		Randomly distribute and pick menu choices for the population
			50%/ plan A
			45%/ plan B
			5%/ plan C

		get count of population
		get count of distribution
		loop through pop count
		assign menu choice
		increment dist count, stop if met
	"""
	# Get counts
	pop = Profile.objects.all()
	pop_count = pop.count() # 954
	a = int(pop_count * a_odds) # 333
	b = int(pop_count * b_odds) # 477
	c = int(pop_count * c_odds) # 143
	if a + b + c is not pop_count:
		remainder = pop_count - a - b - c
		c = c + remainder

	# Set list
	pop_list = []
	for p in pop:
		pop_list.append(p.id)
	random.shuffle(pop_list)
	alist = pop_list[0:a]
	blist = pop_list[a:a+b]
	clist = pop_list[a+b:a+b+c]
	lists = []
	lists.append(alist)
	lists.append(blist)
	lists.append(clist)

	# Loop through and set profile objects
	for i in range(len(lists)):
		for num in lists[i]:
			p = Profile.objects.get(pk=num)
			m = Menu.objects.get(pk=i+1)
			p.choice = m
			p.save()
	print 'Finished setting %s objects' % (pop_count)

	return True