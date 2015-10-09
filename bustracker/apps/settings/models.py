# -*- coding: utf-8 -*-

from django.db import models


class SiteSetting(models.Model):
    ''' Holds site settings values. '''

    STR = 'str'
    BOOL = 'bool'
    INT = 'int'
    FLOAT = 'float'

    SETTING_TYPES = (
        (STR, 'String'),
        (BOOL, 'Boolean'),
        (FLOAT, 'Float'),
        (INT, 'Integer'),
    )

    is_active = models.BooleanField(default=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=800)
    value_type = models.CharField(max_length=10,
                                  choices=SETTING_TYPES,
                                  default=STR)

    def cast(self):
        if self.value_type == SiteSetting.BOOL:
            return bool(self.value)

        if self.value_type == SiteSetting.INT:
            return int(self.value)

        if self.value_type == SiteSetting.FLOAT:
            return float(self.value)

        return self.value
