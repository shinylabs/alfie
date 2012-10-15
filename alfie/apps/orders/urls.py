from django.conf.urls import patterns, url, include

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('alfie.apps.orders.views',
    # show a list of trailers
   	url(r'^order/$', 'startorder'),
)