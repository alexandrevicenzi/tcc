# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.conf import settings
from pymongo import MongoClient, DESCENDING


class Morudall(object):

    def __init__(self):
        uri = 'mongodb://%s:%d/' % (settings.MONGO_ADDRESS, settings.MONGO_PORT)
        mc = MongoClient(uri)
        self.db = mc['morudall']


def get_last_ap_data(device_id):
    return None


def get_last_lat_lon(device_id):
    cursor = Morudall().db.gps_data.find({
        'is_valid': True,
        'device': device_id,
        'latitude': {'$exists': True},
        'longitude': {'$exists': True},
    }).sort('time', DESCENDING).limit(1)

    if cursor.count() > 0:
        return cursor[0]['latitude'], cursor[0]['longitude']

    return None, None


def get_last_velocity(device_id):
    cursor = Morudall().db.gps_data.find({
        'is_valid': True,
        'device': device_id,
        'velocity': {'$exists': True},
    }).sort('time', DESCENDING).limit(1)

    if cursor.count() > 0:
        return cursor[0]['velocity']

    return 0


def get_avg_velocity(device_id, interval=0):
    if interval < 2:
        return get_last_velocity(device_id)

    # TODO: Try map/reduce....
    cursor = Morudall().db.gps_data.find({
        'is_valid': True,
        'device': device_id,
        'velocity': {'$exists': True},
    }).sort('time', DESCENDING).limit(interval)

    velocity = 0.0

    if cursor.count() > 0:
        for item in cursor:
            velocity += item['velocity']
        velocity = velocity / cursor.count()

    return velocity


def get_last_time_online(device_id):
    cursor = Morudall().db.gps_data.find({
        'is_valid': True,
        'device': device_id,
        'latitude': {'$exists': True},
        'longitude': {'$exists': True},
    }).sort('time', DESCENDING).limit(1)

    if cursor.count() > 0:
        return cursor[0]['time']
    return None


def get_last_positions(device_id):
    time = datetime.utcnow() - timedelta(minutes=5)
    cursor = Morudall().db.gps_data.find({
        'is_valid': True,
        'device': device_id,
        'latitude': {'$exists': True},
        'longitude': {'$exists': True},
        'time': {'$gt': time}
    }).sort('time', DESCENDING)

    if cursor.count() > 0:
        for item in cursor:
            yield item['latitude'], item['longitude']

    return


def update_position_ap(device_id, bssid):
    from apps.core.models import BusStop
    stops = BusStop.objects.filter(aps__bssid=bssid)
    if stops.count() > 0:
        data = {
            'device': device_id,
            'time': datetime.now(),
            'latitude': float(stops[0].latitude),
            'longitude': float(stops[0].longitude),
            'is_valid': True,
        }
        Morudall().db.gps_data.insert_one(data)

if __name__ == '__main__':
    import sys

    device_id = sys.argv[1]

    print(get_last_lat_lon(device_id))
    print(get_last_velocity(device_id))
    print(get_avg_velocity(device_id, 10))
    print(get_last_time_online(device_id))
    print(list(get_last_positions(device_id)))
