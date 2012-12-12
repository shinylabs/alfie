from django.conf.urls import patterns, url, include

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('alfie.apps.orders.views',
   	url(r'^order/$', 'start_order', name='start_order'),
   	url(r'^order/cancel/$', 'cancel_order', name='cancel_order'),
    url(r'^order/pay/$', 'pay_order', name='pay_order'),
    url(r'^order/prefs/$', 'save_prefs', name='save_prefs'),
)