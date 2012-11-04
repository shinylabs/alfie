from django.conf.urls import patterns, url, include

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('alfie.apps.users.views',
    # show a list of trailers
    url(r'^signup/$', 'signup'),
   	url(r'^login/$', 'login'),
   	url(r'^logout/$', 'logout'),
)