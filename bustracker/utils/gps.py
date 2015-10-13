# -*- coding: utf-8 -*-

from datetime import datetime
from math import radians, cos, sin, asin, sqrt

HOURS_IN_DAY = 24.0
MINUTES_IN_HOUR = 60.0
MINUTES_IN_DAY = MINUTES_IN_HOUR * HOURS_IN_DAY


class TimeTravel(object):

    def __init__(self, distance, velocity):
        self._value = (float(distance) / float(velocity))

    @property
    def minutes(self):
        return self._value * MINUTES_IN_HOUR

    @property
    def hours(self):
        return (self._value * MINUTES_IN_HOUR) / HOURS_IN_DAY

    @property
    def days(self):
        return self._value * MINUTES_IN_DAY


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


def get_gps_data(device_id):
    # TODO
    return GpsData()


def _haversine1(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points/4913653#4913653
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def _haversine2(lat1, lon1, lat2, lon2):
    # http://rosettacode.org/wiki/Haversine_formula#Python
    R = 6372.8  # Earth radius in kilometers

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2 * asin(sqrt(a))

    return R * c


def distance_from(latitude1, longitude1, latitude2, longitude2):
    '''
        This will return the distance in metters
        between any point and this terminal.

        Haversine formula (https://en.wikipedia.org/wiki/Haversine_formula)
    '''
    return _haversine1(longitude1, latitude1, longitude2, latitude2)


def time_to(distance, velocity):
    '''
    http://www.indiabix.com/aptitude/time-and-distance/formulas

    Args:
        distance: Distance in Kilometers.
        velocity: Velocity in Kilometers per Hour.

    Returns:
        TimeTravel
    '''
    return TimeTravel(distance, velocity)
