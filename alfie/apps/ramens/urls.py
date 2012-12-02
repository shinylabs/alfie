from django.conf.urls import patterns, url, include
from alfie.apps.ramens.views import *

urlpatterns = patterns('',
    url(r'^ramen/$', RamenListView.as_view(), name='ramen_list'),
    url(r'^ramen/add/$', RamenCreateView.as_view(), name='ramen_add'),
    url(r'^ramen/(?P<pk>\d+)/$', RamenDetailView.as_view(), name='ramen_detail'),
    url(r'^ramen/(?P<pk>\d+)/update/$', RamenUpdateView.as_view(), name='ramen_update'),
    url(r'^ramen/(?P<pk>\d+)/delete/$', RamenDeleteView.as_view(), name='ramen_delete'),

    url(r'^ramen/mfg/$', MfgListView.as_view(), name='mfg_list'),
    url(r'^ramen/mfg/add/$', MfgCreateView.as_view(), name='mfg_add'),
    url(r'^ramen/mfg/(?P<pk>\d+)/$', MfgDetailView.as_view(), name='mfg_detail'),
    url(r'^ramen/mfg/(?P<pk>\d+)/update/$', MfgUpdateView.as_view(), name='mfg_update'),
    url(r'^ramen/mfg/(?P<pk>\d+)/delete/$', MfgDeleteView.as_view(), name='mfg_delete'),

    url(r'^ramen/box/$', BoxListView.as_view(), name='box_list'),
    url(r'^ramen/box/add/$', BoxCreateView.as_view(), name='box_add'),
    url(r'^ramen/box/(?P<pk>\d+)/$', BoxDetailView.as_view(), name='box_detail'),
    url(r'^ramen/box/(?P<pk>\d+)/update/$', BoxUpdateView.as_view(), name='box_update'),
    url(r'^ramen/box/(?P<pk>\d+)/delete/$', BoxDeleteView.as_view(), name='box_delete'),
) 