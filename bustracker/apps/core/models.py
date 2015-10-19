# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.ap import get_ap_data, get_distance_from_ap
from utils.gps import get_gps_data, distance_from, time_to


class AccessPoint(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    ap_model = models.CharField(verbose_name=_(u'Modelo'), max_length=250, blank=True, null=True)
    bssid = models.CharField(verbose_name=_(u'BSSID'), max_length=17)
    essid = models.CharField(verbose_name=_(u'ESSID'), max_length=17, blank=True, null=True)
    ssid = models.CharField(verbose_name=_(u'SSID'), max_length=17)
    password = models.CharField(verbose_name=_(u'Senha'), max_length=250)
    frequency = models.FloatField(verbose_name=_(u'Frequência'), help_text=_('Em GHz. Ex: "2.462"'))
    tx_power = models.IntegerField(verbose_name=_(u'TX Power'), blank=True, null=True, help_text=_('Em dBm. Ex: "15"'))
    ieee_802_11_a = models.BooleanField(verbose_name=_(u'802.11a'), default=True)
    ieee_802_11_b = models.BooleanField(verbose_name=_(u'802.11b'), default=True)
    ieee_802_11_g = models.BooleanField(verbose_name=_(u'802.11g'), default=True)
    ieee_802_11_n = models.BooleanField(verbose_name=_(u'802.11n'), default=True)

    def __unicode__(self):
        return '%s - %s' % (self.ssid, self.bssid)

    def get_frequency(self, mode='ghz'):
        conversions = {
            'hz': lambda x: x * 1e+9,
            'khz': lambda x: x * 1000000,
            'mhz': lambda x: x * 1000,
            'ghz': lambda x: x,
        }

        convert = conversions.get(mode.lower())

        if convert:
            return convert(self.frequency)

        raise ValueError('Invalid mode: %s' % mode)


class BusTerminal(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    name = models.CharField(verbose_name=_(u'Nome'), max_length=100)
    details = models.TextField(verbose_name=_(u'Detalhes'), max_length=250, blank=True, null=True)
    latitude = models.DecimalField(verbose_name=_(u'Latitude'), max_digits=12, decimal_places=8)
    longitude = models.DecimalField(verbose_name=_(u'Longitude'), max_digits=12, decimal_places=8)
    aps = models.ManyToManyField(AccessPoint, related_name='ap_set', verbose_name=_(u'APs do Terminal (+)'), blank=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_nearest_terminal(cls, latitude, longitude):
        def distance(t):
            distance = distance_from(float(t.latitude), float(t.longitude), latitude, longitude)
            return distance, t

        # TODO: How we can make this better??
        terminals = BusTerminal.objects.all()

        if len(terminals) > 0:
            return sorted(map(distance, terminals), key=lambda t: t[0])[0][1]

        return None

    def to_dict(self):
        return {
            'id': self.id,
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

    def __unicode__(self):
        return self.name


class Bus(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    name = models.CharField(verbose_name=_(u'Nome'), max_length=100)
    details = models.TextField(verbose_name=_(u'Detalhes'), max_length=250, blank=True, null=True)
    device_id = models.CharField(verbose_name=_(u'ID do Dispositivo'), max_length=17, help_text='MAC Address.')
    route = models.ForeignKey(BusRoute, related_name='bus_set', verbose_name=_(u'Rota'))

    def __unicode__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'device_id': self.device_id,
            'gps_data': self.get_gps_data_cached().to_dict(),
            'ap_data': self.get_ap_data_cached().to_dict(),
            'from_terminal': self.route.from_terminal.name,
            'to_terminal': self.route.to_terminal.name,
            'bus_code': self.route.code,
            'route_name': self.route.name,
        }

    def get_gps_data(self):
        data = get_gps_data(self.device_id)
        # update cached data.
        self._cached_gps_data = data
        return data

    def get_gps_data_cached(self):
        if not hasattr(self, '_cached_gps_data'):
            self._cached_gps_data = self.get_gps_data()

        return self._cached_gps_data

    def get_ap_data(self):
        data = get_ap_data(self.device_id)
        # update cached data.
        self._cached_ap_data = data
        return data

    def get_ap_data_cached(self):
        if not hasattr(self, '_cached_ap_data'):
            self._cached_ap_data = self.get_ap_data()

        return self._cached_ap_data

    def get_estimated_time_to(self, latitude, longitude):
        '''
            Returns the estimated time to the given latitude and longitude
            based on the position of the bus.
        '''
        gps_data = self.get_gps_data_cached()

        if not gps_data:
            return None

        bus_lat, bus_lon = gps_data.latitude, gps_data.longitude
        distance = distance_from(bus_lat, bus_lon, latitude, longitude)

        return time_to(distance, gps_data.velocity)
