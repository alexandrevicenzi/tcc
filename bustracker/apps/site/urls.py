# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='site_index'),
    url(r'^bus-map/$', views.bus_map, name='site_bus_map'),
]
