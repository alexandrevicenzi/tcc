# -*- coding: utf-8 -*-


class GpsData(object):

    def __init__(self, obj=None):
        pass

    @property
    def latitude(self):
        pass

    @property
    def longitude(self):
        pass

    @property
    def last_update(self):
        pass

    @property
    def velocity(self):
        pass


def get_gps_data(device_id):
    return None


def distance_from(latitude1, longitude1, latitude2, longitude2):
    '''
        This will return the distance in metters
        between any point and this terminal.

        Haversine formula (https://en.wikipedia.org/wiki/Haversine_formula)
    '''
    return 0
