# -*- coding: utf-8 -*-

import googlemaps
import requests
import traceback

from math import ceil

try:
    from apps.settings.models import SiteSetting
    API_KEY = SiteSetting.objects.get(key='google_maps_api_key').cast()
except:
    print('Google API KEY not found!')
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


class BaseDirection(object):

    def __init__(self, data):
        self.meters = data['distance']['value']
        self.seconds = data['duration']['value']

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


class Direction(BaseDirection):
    def __init__(self, data):
        data = data[0]['legs'][0]
        super(Direction, self).__init__(data)


class Distance(BaseDirection):

    def __init__(self, data):
        super(Distance, self).__init__(data)


def get_geo_ip(ip):
    if ip:
        try:
            # For better performance, this must be replaced by MaxMind Database.
            res = requests.get('http://www.telize.com/geoip/%s' % ip)

            if res.status_code == 200:
                return LazyObject(**res.json())
        except:
            traceback.print_exc()

    return None


def get_geo_code(latitude, longitude):
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        result = gmaps.reverse_geocode((latitude, longitude))
        return GeoCode(result)
    except:
        traceback.print_exc()

    return None


def get_directions(origin_latitude, origin_longitude, destination_latitude, destination_longitude):
    '''
        Get the distance between to points.
    '''
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        result = gmaps.directions((origin_latitude, origin_longitude), (destination_latitude, destination_longitude),
                                  mode='driving', units='metric', language='pt-BR')
                                  #mode='transit', units='metric', language='pt-BR', transit_mode='bus')
        if len(result) == 1:
            return Direction(result)
    except:
        traceback.print_exc()

    return None


def get_distances(origins, destinations):
    '''
        Get the distances between many points.
        Returns an interpolated dict, where's the key is
        origin and destination (interpolated) and the value is
        the distance between these points.
    '''
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        result = gmaps.distance_matrix(origins, destinations,
                                       mode='driving', units='metric')
                                       #mode='transit', units='metric', transit_mode='bus')
        if result['status'] == 'OK':
            matrix = {}

            for i, origin in enumerate(origins):
                for j, destination in enumerate(destinations):
                    data = result['rows'][i]['elements'][j]
                    if data['status'] == 'OK':
                        matrix[(origin, destination)] = Distance(data)

            if matrix:
                return matrix
    except:
        traceback.print_exc()

    return None


def get_nearest_destination(origin, destinations):
    '''
        Given the origin, discover who is nearest.

        How it works:
            - Calculate the distance between origin and all destinations.
            - Returns the shortest distance to origin.
    '''
    origins = [origin]
    d = get_distances(origins, destinations)

    if d:
        distance = sorted(d.values(), key=lambda item: item.meters)[0]
        key = list(d.keys())[list(d.values()).index(distance)]
        index = destinations.index(key[1])
        return index, distance

    return None, None


if __name__ == '__main__':
    print(get_geo_ip('8.8.8.8').to_dict())
    print(get_geo_code(-26.9115028, -49.081016).to_dict())
    print(get_directions(-26.9115028, -49.081016, -26.8712873, -49.0956086).to_dict())
    origins = [(-26.9115028, -49.081016), (-26.92060830, -49.06775870)]
    destinations = [(-26.8712873, -49.0956086), (-26.96235820, -49.06536180)]
    print(get_distances(origins, destinations))
    print(get_nearest_destination((-26.9115028, -49.081016), destinations))
