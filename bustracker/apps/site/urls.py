# -*- coding: utf-8 -*-

from django.conf.urls import url

from sse_wrapper.views import EventStreamView

from . import views


urlpatterns = [
    url(r'^$', views.index, name='site_index'),
    url(r'^aboout$', views.about, name='site_about'),
    url(r'^bus-stations/$', views.bus_stations, name='site_bus_stations'),
    url(r'^bus-map/$', views.bus_map, name='site_bus_map'),
    url(r'^bus-route/$', views.bus_route, name='site_bus_route'),

    # event stream
    url(r'^bus-near-stream/$',
        EventStreamView.as_view(channel='bus_near'),
        name='bus_near_stream'),

    # event stream
    url(r'^bus-position-stream/$',
        EventStreamView.as_view(channel='bus_position'),
        name='bus_position_stream'),
]
