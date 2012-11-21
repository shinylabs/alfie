from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.static import *
from django.views.generic import TemplateView
from django.conf import settings

from alfie.apps.profiles.forms import SignupFormExtra

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# Local apps
urlpatterns += patterns('',
	url(r'^', include('alfie.apps.front.urls')),
	url(r'^', include('alfie.apps.orders.urls')),
	#url(r'^', include('alfie.apps.profiles.urls')),
)

# Third party apps
urlpatterns += patterns('',
	#original url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra, 'success_url': '/order/pay/'}),
	url(r'^accounts/signup/$', 'alfie.apps.userena.views.signup', {'signup_form': SignupFormExtra, 'success_url': '/order/pay/'}),
	url(r'^accounts/', include('alfie.apps.userena.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
	    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    	}),
	)