from django.contrib import admin
from alfie.apps.ramens.models import *

admin.site.register(Ramen)
admin.site.register(Manufacturer)
admin.site.register(Box)
admin.site.register(Flavor)
admin.site.register(Review)