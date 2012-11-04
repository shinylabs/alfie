from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.static import *
from django.views.generic import TemplateView
from django.conf import settings

from alfie.apps.users.forms import SignupFormExtra

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
	url(r'^', include('alfie.apps.users.urls')),
	url(r'^', include('alfie.apps.orders.urls')),
	#url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
)

# Third party apps
urlpatterns += patterns('',
	url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra, 'success_url': '/pay/'}),
	# url(r'^accounts/user name/signup/complete/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
	url(r'^accounts/', include('userena.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
	    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    	}),
	)