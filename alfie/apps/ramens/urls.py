from django.conf.urls import patterns, url, include
from alfie.apps.ramens.views import *

urlpatterns = patterns('',
    url(r'^ramen/$', RamenListView.as_view(), name='ramen_list'),
    url(r'^ramen/add/$', RamenCreateView.as_view(), name='ramen_add'),
    url(r'^ramen/(?P<pk>\d+)/$', RamenDetailView.as_view(), name='ramen_detail'),
    url(r'^ramen/(?P<pk>\d+)/update/$', RamenUpdateView.as_view(), name='ramen_update'),
    url(r'^ramen/(?P<pk>\d+)/delete/$', RamenDeleteView.as_view(), name='ramen_delete'),

    url(r'^ramen/brands/$', BrandListView.as_view(), name='brand_list'),
    url(r'^ramen/brands/add/$', BrandCreateView.as_view(), name='brand_add'),
    url(r'^ramen/brands/(?P<pk>\d+)/$', BrandDetailView.as_view(), name='brand_detail'),
    url(r'^ramen/brands/(?P<pk>\d+)/update/$', BrandUpdateView.as_view(), name='brand_update'),
    url(r'^ramen/brands/(?P<pk>\d+)/delete/$', BrandDeleteView.as_view(), name='brand_delete'),

    url(r'^ramen/boxes/$', BoxListView.as_view(), name='box_list'),
    url(r'^ramen/boxes/add/$', BoxCreateView.as_view(), name='box_add'),
    url(r'^ramen/boxes/(?P<pk>\d+)/$', BoxDetailView.as_view(), name='box_detail'),
    url(r'^ramen/boxes/(?P<pk>\d+)/update/$', BoxUpdateView.as_view(), name='box_update'),
    url(r'^ramen/boxes/(?P<pk>\d+)/delete/$', BoxDeleteView.as_view(), name='box_delete'),
) 