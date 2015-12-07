# -*- coding: utf-8 -*-

from django.conf.urls import url

from sse_wrapper.views import EventStreamView, SSE_BACKEND_CLASS
from sse_wrapper.utils import class_from_str

from . import views
from utils.morudall import update_position_ap


class CustomEventStreamView(EventStreamView):

    def iterator(self):
        # get the class object from settings (or default if not specified).
        Backend = class_from_str(SSE_BACKEND_CLASS)

        # create a backend instance and subscribe the channel.
        backend = Backend()
        backend.subscribe(self.channel)

        for event, data in backend.listen():
            if event == 'near' and data:
                device_id, ap_bssid = data.split(',')
                try:
                    update_position_ap(device_id, ap_bssid)
                except:
                    pass
            self.sse.add_message(event, data)
            yield


urlpatterns = [
    url(r'^$', views.index, name='site_index'),
    url(r'^aboout$', views.about, name='site_about'),
    url(r'^bus-stations/$', views.bus_stations, name='site_bus_stations'),
    url(r'^bus-map/$', views.bus_map, name='site_bus_map'),
    url(r'^bus-route/$', views.bus_route, name='site_bus_route'),

    # event stream
    url(r'^bus-near-stream/$',
        CustomEventStreamView.as_view(channel='bus_near'),
        name='bus_near_stream'),

    # event stream
    url(r'^bus-position-stream/$',
        EventStreamView.as_view(channel='bus_position'),
        name='bus_position_stream'),
]
