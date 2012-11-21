from django.conf.urls import patterns, url, include

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('alfie.apps.orders.views',
   	url(r'^order/$', 'startOrder'),
   	url(r'^order/cancel/$', 'cancelOrder'),
    url(r'^order/pay/$', 'payOrder'),
    url(r'^order/prefs/$', 'savePrefs'),
)