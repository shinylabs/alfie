from django.db import models

#bigups http://stackoverflow.com/questions/8141460/saving-results-of-django-model-manager-to-database
class Stat(models.Model):
	key = models.CharField(max_length=128, blank=True, null=True)
	value = models.CharField(max_length=128, blank=True, null=True)