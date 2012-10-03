from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.static import *
from django.views.generic import TemplateView
from django.conf import settings

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
	url(r'^', include('alfie.apps.sales.urls')),
	#url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
)

if settings.DEBUG:
	urlpatterns += patterns('',
	    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    	}),
	)