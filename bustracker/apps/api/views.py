# -*- coding: utf-8 -*-

from django.db.models import Q

import apps.core.services as core_service
from apps.core.models import Bus, BusStop
from utils.rest import json_response, token_auth, allow_methods


class Api404(Exception):
    pass


@allow_methods(['GET'])
@token_auth
@json_response
def index(request):
    return 'Bem Vindo %s!' % request.user.username


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus_list(request):
    ''' Return the complete Bus list. '''
    return [bus.to_dict() for bus in list(Bus.objects.filter(is_active=True))]


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus(request, device_id):
    ''' Return the Bus info. '''
    try:
        bus = Bus.objects.get(is_active=True, device_id=device_id)
        return bus.to_dict()
    except Bus.DoesNotExist:
        raise Api404()


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus_by_id(request, bus_id):
    ''' Return the Bus info. '''
    try:
        bus = Bus.objects.get(is_active=True, pk=bus_id)
        return bus.to_dict()
    except Bus.DoesNotExist:
        raise Api404()


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus_stop_list(request):
    ''' Return the complete bus stop list. '''
    return [t.to_dict() for t in list(BusStop.objects.filter(is_active=True))]


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus_station_list(request):
    ''' Return the complete bus station list. '''
    return [t.to_dict() for t in list(BusStop.objects.filter(is_active=True, stop_type='bus-station'))]


@allow_methods(['GET'])
@token_auth
@json_response
def get_nearest_bus_stop(request):
    ''' Return the nearest Terminal
        based on the given latitude and longitude.
    '''
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        nearest = core_service.get_nearest_stop(float(lat), float(lon), ['bus-station'])
        return nearest.to_dict() if nearest else {}

    return {}


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus_stop_bus_list(request, stop_id):
    '''
        Return the Bus list that route pass through or]
        finishes in the given Terminal.
    '''
    bus_list = Bus.objects.filter(Q(route__to_stop__pk=stop_id) | Q(route__stops__pk=stop_id))

    if len(bus_list) > 0:
        return [bus.to_dict() for bus in bus_list]
    else:
        return []


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus_time_list(request, stop_id):
    '''
        Return the time off all Bus that route pass through or
        finishes in the given Terminal.
    '''
    def to_dict(bus, lat, lon):
        return {
            'id': bus.id,
            'code': bus.route.code,
            'name': bus.route.name,
            'time': int(bus.estimated_arrival_to(lat, lon).minutes)
        }

    terminal = BusStop.objects.get(pk=stop_id)
    bus_list = Bus.objects.filter(Q(route__to_stop__pk=stop_id) | Q(route__stops__pk=stop_id))

    if len(bus_list) > 0:
        lat, lon = terminal.latitude, terminal.longitude
        return [to_dict(bus, lat, lon) for bus in bus_list]
    else:
        return []
