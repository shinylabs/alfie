import csv

csvfile = 'alfie/apps/fakers/fakedata/names500.csv'
csvfile2 = 'alfie/apps/fakers/fakedata/names1000.csv'
csvfile3 = 'alfie/apps/fakers/fakedata/names1500.csv'

def load_csv_dict(csvfile):
	"""
	Returns list of data dictionaries
	"""
	reader = csv.DictReader(open(csvfile))
	datarows = []
	for row in reader:
		datarows.append(row)
	return datarows

def load_csv(csvfile='fakedata/biglist10k.csv'):
	"""
	Returns list of header row and data rows
	"""
	reader = csv.reader(open(csvfile))
	datarows = []
	for row in reader:
		datarows.append(row)
	return datarows

def write_csv(data, step=500):
	# Create filename
	fn = 'names' + str(step) + '.csv'
	print 'Creating file %s' % fn

	start=1
	stop=step
	end=len(data)
	files=[]

	while(start < end):
		# Start writer
		writer = csv.writer(open(fn, 'wb'))
		# Write header row
		writer.writerow(data[0])
		
		# Loop through limits
		for row in data[start:stop+1]:
			writer.writerow(row)
		print 'Finished writing\n'

		# Add up files
		files.append(fn)

		# Increment loop
		start+=step
		stop+=step

		# Rename filename
		if start < end:
			fn = 'names' + str(stop) + '.csv'
			print 'Writing new file %s' % fn

	return 'Success, made %s files' % len(files)