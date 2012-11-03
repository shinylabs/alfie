from django.contrib import admin
from django.db import models
from alfie.apps.orders.models import Menu
from django.forms import TextInput, Textarea
import datetime
import sys

admin.site.register(Menu)