import sys
import datetime
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from alfie.apps.orders.models import Menu, Order

class MenuAdmin(admin.ModelAdmin):
	save_on_top = True
	list_display = ('name', 'price')

class OrderAdmin(admin.ModelAdmin):
	save_on_top = True
	list_display = ('id', 'menu', 'user', 'month', 'year', 'paid')

admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)