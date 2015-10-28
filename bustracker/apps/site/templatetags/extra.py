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
    return math.ceil(value)
