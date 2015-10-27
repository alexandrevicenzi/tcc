# -*- coding: utf-8 -*-

from django.conf.urls import url

from sse_wrapper.views import EventStreamView

from . import views


urlpatterns = [
    url(r'^$', views.index, name='site_index'),
    url(r'^bus-map/$', views.bus_map, name='site_bus_map'),

    # event stream
    url(r'^bus-near-stream/$',
        EventStreamView.as_view(channel='bus_near'),
        name='bus_near_stream'),
]
