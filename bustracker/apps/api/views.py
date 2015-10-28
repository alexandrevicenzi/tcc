# -*- coding: utf-8 -*-

from django.db.models import Q

from apps.core.models import Bus, BusTerminal
from utils.rest import json_response, token_auth, allow_methods


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
    return [bus.to_dict() for bus in list(Bus.objects.filter(is_active=True)) if bus.get_gps_data_cached()]


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus(request, device_id):
    ''' Return the Bus info. '''
    try:
        bus = Bus.objects.get(is_active=True, device_id=device_id)
        return bus.to_dict()
    except Bus.DoesNotExist:
        return {}


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus_by_id(request, bus_id):
    ''' Return the Bus info. '''
    try:
        bus = Bus.objects.get(is_active=True, pk=bus_id)
        return bus.to_dict()
    except Bus.DoesNotExist:
        return {}


@allow_methods(['GET'])
@token_auth
@json_response
def get_terminal_list(request):
    ''' Return the complete Terminal list. '''
    return [t.to_dict() for t in list(BusTerminal.objects.filter(is_active=True))]


@allow_methods(['GET'])
@token_auth
@json_response
def get_nearest_terminal(request):
    ''' Return the nearest Terminal
        based on the given latitude and longitude.
    '''
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        nearest = BusTerminal.get_nearest_terminal(float(lat), float(lon))
        return nearest.to_dict() if nearest else {}

    return {}


@allow_methods(['GET'])
@token_auth
@json_response
def get_terminal_bus_list(request, terminal_id):
    '''
        Return the Bus list that route pass through or]
        finishes in the given Terminal.
    '''
    bus_list = Bus.objects.filter(Q(route__to_terminal__pk=terminal_id) | Q(route__terminals__pk=terminal_id))

    if len(bus_list) > 0:
        return [bus.to_dict() for bus in bus_list]
    else:
        return []


@allow_methods(['GET'])
@token_auth
@json_response
def get_bus_time_list(request, terminal_id):
    '''
        Return the time off all Bus that route pass through or
        finishes in the given Terminal.
    '''
    def to_dict(bus, lat, lon):
        return {
            'id': bus.id,
            'code': bus.route.code,
            'name': bus.route.name,
            'time': int(bus.get_estimated_time_to(lat, lon).minutes)
        }

    terminal = BusTerminal.objects.get(pk=terminal_id)
    bus_list = Bus.objects.filter(Q(route__to_terminal__pk=terminal_id) | Q(route__terminals__pk=terminal_id))

    if len(bus_list) > 0:
        lat, lon = terminal.latitude, terminal.longitude
        return [to_dict(bus, lat, lon) for bus in bus_list]
    else:
        return []
