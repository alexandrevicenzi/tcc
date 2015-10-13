# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.gps import get_gps_data


class BusTerminal(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    name = models.CharField(verbose_name=_(u'Nome'), max_length=100)
    details = models.TextField(verbose_name=_(u'Detalhes'), max_length=250, blank=True, null=True)
    latitude = models.DecimalField(verbose_name=_(u'Latitude'), max_digits=12, decimal_places=8)
    longitude = models.DecimalField(verbose_name=_(u'Longitude'), max_digits=12, decimal_places=8)

    def to_dict(self):
        return {
            'name': self.name,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
        }


class BusRoute(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    name = models.CharField(verbose_name=_(u'Nome'), max_length=100)
    details = models.TextField(verbose_name=_(u'Detalhes'), max_length=250, blank=True, null=True)
    code = models.IntegerField(verbose_name=_(u'Código'))
    terminals = models.ManyToManyField(BusTerminal, related_name='route_set', verbose_name=_(u'Terminais de Parada (+)'), blank=True)
    from_terminal = models.ForeignKey(BusTerminal, related_name='from_set', verbose_name=_(u'Terminal de Saída'))
    to_terminal = models.ForeignKey(BusTerminal, related_name='to_set', verbose_name=_(u'Terminal de Chegada'))


class Bus(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    name = models.CharField(verbose_name=_(u'Nome'), max_length=100)
    details = models.TextField(verbose_name=_(u'Detalhes'), max_length=250, blank=True, null=True)
    device_id = models.CharField(verbose_name=_(u'ID do Dispositivo'), max_length=17, help_text='MAC Address.')
    route = models.ForeignKey(BusRoute, related_name='bus_set', verbose_name=_(u'Rota'))

    def to_dict(self):
        return {
            'name': self.name,
            'device_id': self.device_id,
            'gps_data': self.get_gps_data_cached().to_dict(),
            'from_terminal': self.route.from_terminal.name,
            'to_terminal': self.route.to_terminal.name,
            'bus_code': self.route.code,
            'route_name': self.route.name,
        }

    def get_gps_data(self):
        return get_gps_data(self.device_id)

    def get_gps_data_cached(self):
        if not hasattr(self, '_gps_data'):
            self._gps_data = self.get_gps_data()

        return self._gps_data
