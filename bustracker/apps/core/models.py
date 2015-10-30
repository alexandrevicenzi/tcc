# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.geo import get_geo_code, get_directions, get_distances

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
            '''
            Convert frequency to another.

            Args:
                mode:       convert to hz, khz, mhz or ghz (default)
            '''
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

    @property
    def location(self):
        return self.latitude, self.longitude

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'details': self.details,
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
            'details': self.details,
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
            'details': self.details,
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
    def estimated_arrival(self):
        '''
            Returns the estimated time to the arrival latitude and longitude
            based on the position of the bus.
        '''
        lat = self.route.to_stop.latitude
        lon = self.route.to_stop.longitude
        return self.estimated_arrival_to(lat, lon)

    def estimated_arrival_to(self, latitude, longitude):
        '''
            Returns the estimated time to the given latitude and longitude
            based on the position of the bus.
        '''
        if not self.location_available:
            return 0

        bus_lat, bus_lon = self.current_location
        return get_directions(bus_lat, bus_lon, latitude, longitude)

    @property
    def percent_complete_of_route(self):
        '''
            Return the amount (%) which has covered.

            How it works:
                - Get the distance from first stop to the last stop.
                - Get the distance from bus to the last stop.
                - Calculate the remaining in %.
        '''
        if not self.location_available:
            return 0.0

        bus_lat = self.gps_data_cached.latitude
        bus_lon = self.gps_data_cached.longitude
        from_lat = self.route.from_stop.latitude
        from_lon = self.route.from_stop.longitude
        to_lat = self.route.to_stop.latitude
        to_lon = self.route.to_stop.longitude

        from_distance_to = get_directions(from_lat, from_lon, to_lat, to_lon).meters
        bus_distance = get_directions(bus_lat, bus_lon, to_lat, to_lon).meters

        d = from_distance_to - bus_distance
        return d * 100 / from_distance_to

    @property
    def location_available(self):
        if self.gps_data:
            return True
        return False

    @property
    def current_location(self):
        if not self.location_available:
            return None, None

        return self.gps_data_cached.latitude, self.gps_data_cached.longitude

    @property
    def current_location_info(self):
        if not self.location_available:
            return None

        return get_geo_code(*self.current_location)

    @property
    def next_stop(self):
        '''
            Discover who is the next stop.

            How it works:
                - Calculate Bus distante from last stop.
                - Calculate all distances between all stops and last stop.
                - Get the stop that is more far from last stop and the stop distance
                  is smaller then bus distance from last stop.
                - If there's none between, return the last stop.
        '''
        if not self.location_available:
            return None

        stops = self.route.stops.all()

        if stops.count() > 0:
            bus_lat, bus_lon = self.current_location
            to_lat, to_lon = self.route.to_stop.location
            bus_distance = get_directions(bus_lat, bus_lon, to_lat, to_lon).meters

            pos_list = [(x.latitude, x.longitude) for x in stops]
            distances = get_distances([(to_lat, to_lon)], pos_list)

            if distances:
                d = distances.values()
                nexts = filter(lambda d: d.meters < bus_distance, d)

                if len(nexts) > 0:
                    distance = sorted(nexts, key=lambda item: item.meters)[0]
                    key = distances.keys()[distances.values().index(distance)]
                    index = pos_list.index(key[1])
                    return stops[index]

        return self.route.to_stop

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
