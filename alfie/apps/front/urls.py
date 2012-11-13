from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('alfie.apps.front.views',
   	url(r'^$', TemplateView.as_view(template_name="front/index.html"), name="index"),
)