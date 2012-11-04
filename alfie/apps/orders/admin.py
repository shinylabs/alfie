from django.contrib import admin
from django.db import models
from alfie.apps.orders.models import Menu, Order
from django.forms import TextInput, Textarea
import datetime
import sys

class MenuAdmin(admin.ModelAdmin):
	save_on_top = True
	list_display = ('name', 'price')

class OrderAdmin(admin.ModelAdmin):
	save_on_top = True
	list_display = ('id', 'plan', 'user', 'month', 'year')

admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)