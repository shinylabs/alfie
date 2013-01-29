from django.conf.urls import patterns, url, include

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('alfie.apps.back.views',
   	url(r'^back/$', 'backoffice', name="backoffice"),
   	url(r'^back/inventory/$', 'inventory_index', name="inventory"),
   	url(r'^back/orders/$', 'orders_index', name="orders"),
   	url(r'^back/finances/$', 'finances_index', name="finances"),
   	url(r'^back/shipping/$', 'shipping_index', name="shipping"),
   	url(r'^back/customers/$', 'customers_index', name="customers"),

   	#url(r'^back/tools/finance/$', 'finance_tools', name="finance_tools"),
   	#url(r'^back/tools/finance/coupon/$', 'finance_coupon', name="finance_coupon"),
   	#url(r'^back/tools/logistics/$', 'logistics_tools', name="logistics_tools"),
)


"""

/back
     /inventory
     /inventory/brand/{CRUD}
     /inventory/ramen/{CRUD}
     /inventory/box/{CRUD}
     /finances
     /shipping
     /customers

"""