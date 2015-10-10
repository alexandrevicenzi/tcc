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
    return list(Bus.objects.filter(is_active=True))


@allow_methods(['GET'])
@token_auth
@json_response
def get_terminal_list(request):
    def to_dict(obj):
        return {
            'name': obj.name,
            'latitude': float(obj.latitude),
            'longitude': float(obj.longitude),
        }

    return [to_dict(t) for t in list(BusTerminal.objects.filter(is_active=True))]
