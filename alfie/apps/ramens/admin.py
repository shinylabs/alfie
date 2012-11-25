from django.contrib import admin
from alfie.apps.ramens.models import Ramen, Manufacturer, Flavor, Review, Box, Membership

admin.site.register(Ramen)
admin.site.register(Manufacturer)
admin.site.register(Flavor)
admin.site.register(Review)
admin.site.register(Box)
admin.site.register(Membership)