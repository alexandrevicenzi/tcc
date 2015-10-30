# -*- coding: utf-8 -*-

from datetime import datetime

from utils.geo import get_geo_ip, get_nearest_destination


class GpsData(object):

    def __init__(self, obj=None):
        pass

    @property
    def latitude(self):
        # TODO
        return -26.9115028

    @property
    def longitude(self):
        # TODO
        return -49.081016

    @property
    def last_update(self):
        # TODO
        return datetime.now()

    @property
    def velocity(self):
        # TODO:
        return 60.0

    def to_dict(self):
        if self.last_update.date() < datetime.now().date():
            last_update = self.last_update.strftime('%d/%m/%Y')
        else:
            last_update = self.last_update.strftime('%H:%M')

        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'last_update': last_update,
            'velocity': self.velocity,
        }


class ApData(object):

    def __init__(self, obj=None):
        ip = ''
        self._geo_ip = get_geo_ip(ip)

    @property
    def latitude(self):
        return self._geo_ip.get('latitude')

    @property
    def longitude(self):
        return self._geo_ip.get('longitude')

    @property
    def last_update(self):
        # TODO
        return datetime.now()

    @property
    def rssi(self):
        # TODO
        return 0

    @property
    def bssid(self):
        # TODO
        return ''

    def to_dict(self):
        if self.last_update.date() < datetime.now().date():
            last_update = self.last_update.strftime('%d/%m/%Y')
        else:
            last_update = self.last_update.strftime('%H:%M')

        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'last_update': last_update,
            'bssid': self.bssid,
        }


def get_nearest_stop(latitude, longitude, kinds=None):
    from .models import BusStop
    # TODO: Flat select is better...
    stops = BusStop.objects.all()

    if kinds:
        stops = stops.filter(stop_type__in=kinds)

    if stops.count() > 0:
        pos_list = [(x.latitude, x.longitude) for x in stops]
        index, _ = get_nearest_destination((latitude, longitude), pos_list)
        return stops[index]

    return None


def get_last_gps_data(device_id):
    return GpsData()


def get_last_ap_data(device_id):
    return None
