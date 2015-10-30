# -*- coding: utf-8 -*-

import googlemaps
import requests

from math import ceil

try:
    from apps.settings.models import SiteSetting
    API_KEY = SiteSetting.objects.get(key='google_maps_api_key').cast()
except Exception as e:
    print(str(e))
    API_KEY = ''


class LazyObject(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return self.__dict__


class GeoCode(object):

    def __init__(self, data):
        self._address_components = data[0]['address_components']

    def get_component(self, name, short=False):
        attr_name = '_%s' % name
        if not hasattr(self, attr_name):
            for component in self._address_components:
                if name in component['types']:
                    value = component['short_name'] if short else component['long_name']
                    setattr(self, attr_name, value)

        return getattr(self, attr_name)

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


class Direction(object):

    def __init__(self, data):
        route = data[0]['legs'][0]
        self.meters = route['distance']['value']
        self.seconds = route['duration']['value']

    @property
    def minutes(self):
        return ceil(self.seconds / 60)

    @property
    def hours(self):
        return round(self.seconds / 60 / 60, 1)

    @property
    def km(self):
        return round(self.meters / 1000, 1)

    def to_dict(self):
        return {
            'meters': self.meters,
            'seconds': self.seconds,
            'minutes': self.minutes,
            'hours': self.hours,
            'km': self.km
        }


def get_geo_ip(ip):
    if ip:
        try:
            # For better performance, this must be replaced by MaxMind Database.
            res = requests.get('http://www.telize.com/geoip/%s' % ip)

            if res.status_code == 200:
                return LazyObject(**res.json())
        except Exception as e:
            print(str(e))

    return None


def get_geo_code(latitude, longitude):
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        result = gmaps.reverse_geocode((latitude, longitude))
        return GeoCode(result)
    except Exception as e:
        print(str(e))

    return None


def get_directions(origin_latitude, origin_longitude, destination_latitude, destination_longitude):
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        result = gmaps.directions((origin_latitude, origin_longitude), (destination_latitude, destination_longitude),
                                  mode='driving', units='metric', language='pt-BR')
                                  #mode='transit', units='metric', language='pt-BR', transit_mode='bus')
        if len(result) == 1:
            return Direction(result)
    except Exception as e:
        print(str(e))

    return None


if __name__ == '__main__':
    print(get_geo_ip('8.8.8.8').to_dict())
    print(get_geo_code(-26.9115028, -49.081016).to_dict())
    print(get_directions(-26.9115028, -49.081016, -26.8712873, -49.0956086).to_dict())
