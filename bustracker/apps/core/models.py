# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.geo import get_geo_code
from utils.calc import convert_frequency, distance_from, time_to

from .services import get_last_ap_data, get_last_gps_data


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
        return convert_frequency(self.frequency, mode)

    def to_dict(self):
        return {
            'ssid': self.ssid,
            'bssid': self.bssid,
        }


class BusStop(models.Model):

    BUS_STOP = 'bus-stop'
    BUS_STATION = 'bus-station'
    GARAGE = 'garage'

    STOP_TYPES = (
        (BUS_STOP, _(u'Ponto')),
        (BUS_STATION, _(u'Terminal')),
        (GARAGE, _(u'Garagem')),
    )

    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    name = models.CharField(verbose_name=_(u'Nome'), max_length=100)
    details = models.TextField(verbose_name=_(u'Detalhes'), max_length=250, blank=True, null=True)
    latitude = models.DecimalField(verbose_name=_(u'Latitude'), max_digits=12, decimal_places=8)
    longitude = models.DecimalField(verbose_name=_(u'Longitude'), max_digits=12, decimal_places=8)
    aps = models.ManyToManyField(AccessPoint, related_name='ap_set', verbose_name=_(u'APs do Terminal (+)'), blank=True)
    stop_type = models.CharField(max_length=15,
                                 choices=STOP_TYPES,
                                 default=BUS_STATION)

    def __unicode__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'type': self.stop_type,
            'aps': [x.to_dict() for x in self.aps.filter(is_active=True)]
        }


class BusRoute(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    name = models.CharField(verbose_name=_(u'Nome'), max_length=100)
    details = models.TextField(verbose_name=_(u'Detalhes'), max_length=250, blank=True, null=True)
    code = models.IntegerField(verbose_name=_(u'Código'))
    stops = models.ManyToManyField(BusStop, related_name='stops_set', verbose_name=_(u'Terminais de Parada (+)'), blank=True)
    from_stop = models.ForeignKey(BusStop, related_name='from_set', verbose_name=_(u'Terminal de Saída'))
    to_stop = models.ForeignKey(BusStop, related_name='to_set', verbose_name=_(u'Terminal de Chegada'))

    def __unicode__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'from': self.from_stop.to_dict(),
            'to': self.to_stop.to_dict(),
            'stops': [x.to_dict() for x in self.stops.filter(is_active=True)]
        }


class Bus(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    name = models.CharField(verbose_name=_(u'Nome'), max_length=100)
    details = models.TextField(verbose_name=_(u'Detalhes'), max_length=250, blank=True, null=True)
    device_id = models.CharField(verbose_name=_(u'ID do Dispositivo'), max_length=17, help_text='MAC Address.')
    route = models.ForeignKey(BusRoute, related_name='bus_set', verbose_name=_(u'Rota'))

    def __unicode__(self):
        return self.name

    def to_dict(self):
        lat, lon = self.current_location
        return {
            'id': self.id,
            'name': self.name,
            'device_id': self.device_id,
            'route': self.route.to_dict(),
            'latitude': lat,
            'longitude': lon,
            'velocity': self.avg_velocity,
        }

    @property
    def gps_data(self):
        data = get_last_gps_data(self.device_id)
        # update cached data.
        self._cached_gps_data = data
        return data

    @property
    def gps_data_cached(self):
        if not hasattr(self, '_cached_gps_data'):
            return self.gps_data

        return self._cached_gps_data

    @property
    def ap_data(self):
        data = get_last_ap_data(self.device_id)
        # update cached data.
        self._cached_ap_data = data
        return data

    @property
    def ap_data_cached(self):
        if not hasattr(self, '_cached_ap_data'):
            return self.ap_data

        return self._cached_ap_data

    @property
    def estimated_time_arrival(self):
        '''
            Returns the estimated time to the arrival latitude and longitude
            based on the position of the bus.
        '''
        lat = self.route.to_stop.latitude
        lon = self.route.to_stop.longitude
        return self.estimated_time_to(lat, lon)

    def estimated_time_to(self, latitude, longitude):
        '''
            Returns the estimated time to the given latitude and longitude
            based on the position of the bus.
        '''
        if not self.gps_data_cached:
            return None

        bus_lat, bus_lon = self.gps_data_cached.latitude, self.gps_data_cached.longitude
        distance = distance_from(bus_lat, bus_lon, latitude, longitude)

        return time_to(distance, self.gps_data_cached.velocity)

    @property
    def percent_complete_of_route(self):
        if not self.gps_data:
            return 0.0

        bus_lat = self.gps_data.latitude
        bus_lon = self.gps_data.longitude
        from_lat = self.route.from_stop.latitude
        from_lon = self.route.from_stop.longitude
        to_lat = self.route.to_stop.latitude
        to_lon = self.route.to_stop.longitude

        from_distance_to = distance_from(from_lat, from_lon, to_lat, to_lon)
        bus_distance = distance_from(bus_lat, bus_lon, to_lat, to_lon)

        d = from_distance_to - bus_distance
        return d * 100 / from_distance_to

    @property
    def current_location(self):
        gps_data = self.gps_data_cached

        if not gps_data:
            return None

        return gps_data.latitude, gps_data.longitude

    @property
    def current_location_info(self):
        bus_lat, bus_lon = self.current_location

        if not bus_lat or bus_lon:
            return None

        return get_geo_code(bus_lat, bus_lon)

    @property
    def avg_velocity(self):
        return 60

    @property
    def is_online(self):
        return True

    @property
    def is_moving(self):
        return True

    @property
    def is_parked(self):
        return False
