# -*- coding: utf-8 -*-

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
    return [bus.to_dict() for bus in list(Bus.objects.filter(is_active=True)) if bus.get_gps_data_cached()]


@allow_methods(['GET'])
@token_auth
@json_response
def get_terminal_list(request):
    return [t.to_dict() for t in list(BusTerminal.objects.filter(is_active=True))]


@allow_methods(['GET'])
@token_auth
@json_response
def get_nearest_terminal(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        nearest = BusTerminal.get_nearest_terminal(float(lat), float(lon))
        return nearest.to_dict() if nearest else {}

    return {}
