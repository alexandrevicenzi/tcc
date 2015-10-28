# -*- coding: utf-8 -*-

import requests


class GeoCode(object):

    def __init__(self, address_components):
        self._address_components = address_components

    def get_component(self, name, short=False):
        if not hasattr(self, name):
            for component in self._address_components:
                if name in component['types']:
                    value = component['short_name'] if short else component['long_name']
                    setattr(self, name, value)

        return getattr(self, name)

    @property
    def street_name(self):
        return self.get_component('route')

    @property
    def district(self):
        return self.get_component('sublocality')

    @property
    def city(self):
        return self.get_component('locality')

    @property
    def state(self):
        return self.get_component('administrative_area_level_1')

    @property
    def state_code(self):
        return self.get_component('administrative_area_level_1', True)

    @property
    def country(self):
        return self.get_component('country')

    @property
    def country_code(self):
        return self.get_component('country', True)

    def to_dict(self):
        return {
            'street_name': self.get_component('route'),
            'district': self.get_component('sublocality'),
            'city': self.get_component('locality'),
            'state': self.get_component('administrative_area_level_1'),
            'state_code': self.get_component('administrative_area_level_1', True),
            'country': self.get_component('country'),
            'country_code': self.get_component('country', True),
        }


def get_geo_ip_data(ip):
    if ip:
        try:
            # For better performance, this must be replaced by MaxMind Database.
            res = requests.get('http://www.telize.com/geoip/%s' % ip)

            if res.status_code == 200:
                return res.json()
        except:
            pass

    return {}


def get_geo_code(latitude, longitude):
    try:
        res = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f&sensors=true' % (latitude, longitude))

        if res.status_code == 200:
            payload = res.json()
            if payload['status'] == 'OK':
                result = payload['results'][0]['address_components']
                return GeoCode(result)
    except:
        pass

    return None

if __name__ == '__main__':
    print(get_geo_code(-26.9115028, -49.081016).to_dict())
