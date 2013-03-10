<<<<<<< HEAD
web: gunicorn -c gunicorn.py.ini wsgi:application
=======
web: newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi:application 
>>>>>>> r7-datacleanse
scheduler: python manage.py celeryd -B -E --maxtasksperchild=1000
worker: python manage.py celeryd -E --maxtasksperchild=1000
