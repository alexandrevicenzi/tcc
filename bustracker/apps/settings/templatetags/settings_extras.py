# -*- coding: utf-8 -*-

from django import template

from apps.settings.models import SiteSetting

register = template.Library()


class SettingNameNotFound(Exception):

    def __init__(self, name):
        super(SettingNameNotFound, self).__init__(
            'Setting %s not found. Be sure it\'s configured.' % name)


@register.simple_tag
def setting(name, raises=True, default=None):
    if not name:
        raise ValueError('Invalid setting name.')

    try:
        setting = SiteSetting.objects.get(key=name)
        return setting.cast()
    except SiteSetting.DoesNotExist:
        if raises:
            raise SettingNameNotFound(name)

        return default
