# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


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

    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    key = models.CharField(verbose_name=_(u'Chave'), max_length=100)
    value = models.CharField(verbose_name=_(u'Valor'), max_length=800)
    value_type = models.CharField(verbose_name=_(u'Tipo'),
                                  max_length=10,
                                  choices=SETTING_TYPES,
                                  default=STR)

    def __unicode__(self):
        return self.key

    def cast(self):
        if self.value_type == SiteSetting.BOOL:
            return bool(self.value)

        if self.value_type == SiteSetting.INT:
            return int(self.value)

        if self.value_type == SiteSetting.FLOAT:
            return float(self.value)

        return self.value

    class Meta:
        verbose_name = _(u'Configuração do Sistema')
        verbose_name_plural = _(u'Configurações do Sistema')
