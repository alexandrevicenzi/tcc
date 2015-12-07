# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import reduce

from utils.geo import get_nearest_destination, get_distances
from utils.morudall import get_last_lat_lon, get_avg_velocity, get_last_time_online, get_last_positions


def get_nearest_stop(latitude, longitude, kinds=None):
    from .models import BusStop
    # TODO: Flat select is better...
    stops = BusStop.objects.all()

    if kinds:
        stops = stops.filter(stop_type__in=kinds)

    if stops.count() > 0:
        pos_list = [(x.latitude, x.longitude) for x in stops]
        index, distance = get_nearest_destination((latitude, longitude), pos_list)
        return stops[index], distance

    return None, None


def current_location(device_id):
    return get_last_lat_lon(device_id)


def avg_velocity(device_id):
    '''
        Returns the average velocity from the
        last 10 (if available) data collected.
    '''
    return get_avg_velocity(device_id, 10)


def is_online(device_id):
    '''
        Returns True if the Bus was online in
        the past 5 minutes.
    '''

    time = get_last_time_online(device_id)

    if time:
        min_time = datetime.utcnow() - timedelta(minutes=5)
        return time > min_time

    return False


def is_moving(device_id):
    '''
        Returns True if the Bus has moved
        more then 250m in the last 5 minutes.
    '''
    lat, lon = get_last_lat_lon(device_id)
    positions = list(get_last_positions(device_id))

    if lat and lon and positions:
        distances = get_distances([(lat, lon)], positions)
        distances = list(distances.values())
        distance = reduce(lambda acc, item: acc + item.meters, distances) / len(positions)
        return distance > 250

    return False


def is_parked(device_id):
    '''
        Returns true if the Bus is not is_moving
        and is less then 250m from any station
        or garage.
    '''
    if not is_moving(device_id):
        lat, lon = current_location(device_id)
        if lat and lon:
            stop, distance = get_nearest_stop(lat, lon, ['bus-station', 'garage'])
            if stop:
                return distance < 250

    return False
