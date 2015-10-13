# -*- coding: utf-8 -*-

from datetime import datetime


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


def distance_from(latitude1, longitude1, latitude2, longitude2):
    '''
        This will return the distance in metters
        between any point and this terminal.

        Haversine formula (https://en.wikipedia.org/wiki/Haversine_formula)
    '''
    # TODO
    return 0
