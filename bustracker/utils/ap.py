# -*- coding: utf-8 -*-

import requests

from datetime import datetime
from math import log10


def get_geo_ip_data(ip):
    if not ip:
        return {}

    try:
        # For better performance, this must be replaced by MaxMind Database.
        res = requests.get('http://www.telize.com/geoip/%s' % ip)
        if res.status_code == 200:
            return res.json()
        else:
            return {}
    except:
        return {}


def get_distance_from_ap(db, frequency):
    '''
        This will return the distance from an AP in metters
        based on his signal strenght.

        Free-space path loss formula (https://en.wikipedia.org/wiki/Free-space_path_loss).
    '''
    # 92.45 for GHz and km
    # -87.55 for meters and kHz
    # -27.55 for meters and mHz
    # 32.45 for km and mHz
    return 10 ** ((27.55 - (20 * log10(frequency)) + db) / 20)


class ApData(object):

    def __init__(self, obj=None):
        ip = ''
        self._geo_ip = get_geo_ip_data(ip)

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


def get_ap_data(device_id):
    return ApData()
