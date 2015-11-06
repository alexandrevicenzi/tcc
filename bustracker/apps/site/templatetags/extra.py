# -*- coding: utf-8 -*-
import math

from django import template
from django.core.urlresolvers import reverse
from django.utils.http import urlquote

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, name, **kwargs):
    request = context['request']

    if reverse(name, kwargs=kwargs) == urlquote(request.path):
        return 'active'

    return ''


@register.filter('ceil')
def do_ceil(value):
    if not value:
        return 0
    return math.ceil(value)


@register.filter()
def estimated_arrival_to(bus, station):
    if not station:
        return 0.0

    try:
        return bus.estimated_arrival_to(station.latitude, station.longitude).minutes
    except:
        return 0.0
