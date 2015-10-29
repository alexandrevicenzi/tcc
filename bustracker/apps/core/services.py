# -*- coding: utf-8 -*-

from datetime import datetime

from utils.calc import distance_from


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


def get_nearest_stop(latitude, longitude, kind=None):
    def distance(t):
        distance = distance_from(float(t.latitude), float(t.longitude), latitude, longitude)
        return distance, t

    # TODO: How we can make this better??
    from .models import BusStop
    stops = BusStop.objects.all()

    if kind:
        stops = stops.filter(stop_type=kind)

    if len(stops) > 0:
        return sorted(map(distance, stops), key=lambda t: t[0])[0][1]

    return None


def get_last_gps_data(device_id):
    return GpsData()


def get_last_ap_data(device_id):
    return None
