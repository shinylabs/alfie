from django.conf.urls import patterns, url, include

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('alfie.apps.back.views',
   	url(r'^office/$', 'backoffice', name="backoffice"),

   	url(r'^office/tools/finance/$', 'finance_tools', name="finance_tools"),
   	url(r'^office/tools/finance/coupon/$', 'finance_coupon', name="finance_coupon"),

   	url(r'^office/tools/logistics/$', 'logistics_tools', name="logistics_tools"),
)