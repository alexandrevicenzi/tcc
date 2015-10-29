# -*- coding: utf-8 -*-

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


def convert_frequency(frequency, mode='ghz'):
    '''
    Convert frequency to another.

    Args:
        frequency:  value in ghz
        mode:       convert to hz, khz, mhz or ghz (default)
    '''
    conversions = {
        'hz': lambda x: x * 1e+9,
        'khz': lambda x: x * 1000000,
        'mhz': lambda x: x * 1000,
        'ghz': lambda x: x,
    }

    convert = conversions.get(mode.lower())

    if convert:
        return convert(frequency)

    raise ValueError('Invalid mode: %s' % mode)


def haversine(lon1, lat1, lon2, lat2):
    ''''
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees).

    Args:
        lon1:
        lat1:
        lon2:
        lat2:

    Returns:
        The distance in Km.

    See:
        http://rosettacode.org/wiki/Haversine_formula
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    R = 6372.8
    return c * R


def distance_from(latitude1, longitude1, latitude2, longitude2):
    '''
        This will return the distance in metters
        between any point and this terminal.

        Haversine formula (https://en.wikipedia.org/wiki/Haversine_formula)
    '''
    return haversine(longitude1, latitude1, longitude2, latitude2)


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
