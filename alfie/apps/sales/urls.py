from django.conf.urls import patterns, url, include

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('alfie.apps.sales.views',
    # show a list of trailers
    url(r'^', 'index', name='sales_index'),
)