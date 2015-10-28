# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^api/$', views.index, name='api_index'),
    url(r'^api/bus/$', views.get_bus_list, name='api_bus_list'),
    url(r'^api/bus/(?P<device_id>[0-9a-zA-Z:-]+)$', views.get_bus, name='api_bus_info'),
    url(r'^api/bus/(?P<bus_id>[0-9]+)$', views.get_bus_by_id, name='api_bus_info_by_id'),
    url(r'^api/terminal/$', views.get_terminal_list, name='api_terminal_list'),
    url(r'^api/terminal/(?P<terminal_id>[0-9]+)/bus$', views.get_terminal_bus_list, name='api_terminal_bus_list'),
    url(r'^api/terminal/(?P<terminal_id>[0-9]+)/bus-time$', views.get_bus_time_list, name='api_bus_time_list'),
    url(r'^api/nearest/terminal/$', views.get_nearest_terminal, name='api_nearest_terminal'),
]
