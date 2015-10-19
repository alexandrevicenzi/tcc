# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^api/$', views.index, name='api_index'),
    url(r'^api/bus/$', views.get_bus_list, name='api_bus_list'),
    url(r'^api/terminal/$', views.get_terminal_list, name='api_terminal_list'),
    url(r'^api/terminal/(?P<terminal_id>[0-9]+)/bus$', views.get_terminal_bus_list, name='api_terminal_bus_list'),
    url(r'^api/terminal/(?P<terminal_id>[0-9]+)/bus-time$', views.get_bus_time_list, name='api_bus_time_list'),
    url(r'^api/nearest/terminal/$', views.get_nearest_terminal, name='api_nearest_terminal'),
]
