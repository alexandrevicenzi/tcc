# -*- coding: utf-8 -*-

#
# NMEA 0183 2.3 Parser implementation
#
# This module implements only GGA, GLL and VTG sentences.
#
#
# NMEA 0183 Protocol References
#
# https://www.sparkfun.com/datasheets/GPS/NMEA%20Reference%20Manual1.pdf
# http://www.plaisance-pratique.com/IMG/pdf/NMEA0183-2.pdf
# http://www.tronico.fi/OH6NT/docs/NMEA0183.pdf
#

import re

from datetime import date, time


class ParseException(Exception):
    pass


class UTCTimeParser(object):
    '''
        Convert string UTC Time into datetime.time.
        It must follow the format hhmmss (161229) or hhmmss.sss (161229.487).
    '''

    def __new__(cls, value):
        try:
            h, m, s, _, ms = re.match(r'^(\d{2})(\d{2})(\d{2})(\.(\d+))?$', value).groups()
            ms = ms or 0
            return time(int(h), int(m), int(s), int(ms))
        except:
            raise ParseException('Can\'t parse value into UTC Time: %s' % value)


class DateParser(object):

    def __new__(cls, value):
        try:
            d, m, y = re.match(r'^(\d{2})(\d{2})(\d{2})$', value).groups()
            y = '20%s' % y
            return date(int(y), int(m), int(d))
        except Exception, e:
            raise ParseException('Can\'t parse value into Date: %s' % value)


class SentenceMixin(object):

    def to_dict(self):
        return {}


class Sentence(object):
    sentence = 'Unknown'
    sentence_description = 'Unknown Sentence'
    fields = ()

    def __init__(self):
        self._fields_count = len(self.fields)
        self._last = self._fields_count - 1

    def parse(self, data):
        raw_fields = data.split(',')

        if len(raw_fields) != self._fields_count:
            raise ParseException('Field count mismatch. Expected %d fields, but found %d.' % (self._fields_count, len(raw_fields)))

        for index, field in enumerate(self.fields):
            field_name, _, field_type = field
            try:
                value = raw_fields[index]
                value = value.strip()

                if value:
                    if index == self._last:
                        value, checksum = value.split('*')

                    setattr(self, field_name, field_type(value))
                else:
                    setattr(self, field_name, None)
            except:
                raise ParseException('Can\'t parse value into field "%s": %s' % (field_name, value))

        return self

    @property
    def is_valid(self):
        return False

    def to_dict(self):
        d = {key: self.__dict__[key] for key, _, _ in self.fields}

        d.update({
            'sentence': self.sentence_name,
            'is_valid': self.is_valid
        })

        if isinstance(self, SentenceMixin):
            # Ignore first class, is itself (avoid recursion loop).
            # Ignore last class, is object.
            base_classes = [cls for cls in self.__class__.__mro__[1:-1] if issubclass(cls, SentenceMixin)]

            for cls in base_classes:
                d.update(cls.to_dict(self))

        return d


class LatLonMixin(SentenceMixin):

    def _convert_lat_lon(self, value):
        '''
        Convert Latitude/Longitude NMEA format to
        Python float degree.

        Args:
            value: ddmm.mmmm
        '''
        d, m = re.match(r'^(\d+)(\d\d\.\d+)$', value).groups()
        return float(d) + float(m) / 60

    @property
    def latitude_degree(self):
        lat = self._convert_lat_lon(self.latitude)

        if self.ns_indicator == 'S':
            return abs(lat) * -1

        return abs(lat)

    @property
    def longitude_degree(self):
        lon = self._convert_lat_lon(self.longitude)

        if self.ew_indicator == 'W':
            return abs(lon) * -1

        return abs(lon)

    def to_dict(self):
        return {
            'latitude_degree': self.latitude_degree,
            'longitude_degree': self.longitude_degree,
        }


class KnotToKmHMixin(SentenceMixin):

    @property
    def speed_km_h(self):
        return self.speed_over_ground * 1.852

    def to_dict(self):
        return {
            'speed_km_h': self.speed_km_h,
        }


class GGASentence(Sentence, LatLonMixin):
    sentence_name = 'GGA'
    sentence_description = 'Global Positioning System Fix Data'
    fields = (
        ('utc_time', 'UTC Time', UTCTimeParser),
        ('latitude', 'Latitude', str),
        ('ns_indicator', 'N/S Indicator', str.upper),
        ('longitude', 'Longitude', str),
        ('ew_indicator', 'E/W Indicator', str.upper),
        ('fix_quality', 'Position Fix Indicator', int),
        ('num_satellites', 'Satellites Used', int),
        ('hdop', 'Horizontal Dilution of Precision', float),
        ('msl_altitude', 'MSL Altitude', float),
        ('msl_units', 'MSL Altitude Units', str),
        ('geoid_separation', 'Geoid Separation', float),
        ('geoid_sep_units', 'Geoid Separation Units', str),
        ('age_diff', 'Age of Differential GPS data', float),
        ('station_id', 'Differential reference station ID', str),
    )

    def __init__(self):
        super(GGASentence, self).__init__()

    @property
    def is_valid(self):
        return self.fix_quality in [1, 2]


class GLLSentence(Sentence, LatLonMixin):
    sentence_name = 'GLL'
    sentence_description = 'Geographic Position – Latitude/Longitude'
    fields = (
        ('latitude', 'Latitude', str),
        ('ns_indicator', 'N/S Indicator', str.upper),
        ('longitude', 'Longitude', str),
        ('ew_indicator', 'E/W Indicator', str.upper),
        ('utc_time', 'UTC Time', UTCTimeParser),
        ('status', 'Status', str.upper),
        # ('mode', 'Mode', str), NMEA V 3.00
    )

    def __init__(self):
        super(GLLSentence, self).__init__()

    @property
    def is_valid(self):
        return self.status == 'A'


class RMCSentence(Sentence, LatLonMixin, KnotToKmHMixin):
    sentence_name = 'RMC'
    sentence_description = 'Recommended Minimum Specific GNSS Data'
    fields = (
        ('utc_time', 'UTC Time', UTCTimeParser),
        ('status', 'Status', str.upper),
        ('latitude', 'Latitude', str),
        ('ns_indicator', 'N/S Indicator', str.upper),
        ('longitude', 'Longitude', str),
        ('ew_indicator', 'E/W Indicator', str.upper),
        ('speed_over_ground', 'Speed Over Ground (knots)', float),
        ('course_over_ground', 'Course Over Ground (degrees)', float),
        ('data', 'Date', DateParser),
        ('magnetic_variation', 'E/W Indicator', str.upper),
        # ('mode', 'Mode', str), NMEA V 3.00
    )

    def __init__(self):
        super(RMCSentence, self).__init__()

    @property
    def is_valid(self):
        return self.status == 'A'


class VTGSentence(Sentence):
    sentence_name = 'VTG'
    sentence_description = 'Course Over Ground and Ground Speed'
    fields = (
        ('course_1', 'Measured heading', float),
        ('reference_1', 'Reference', str),
        ('course_1', 'Measured heading', float),
        ('reference_2', 'Reference', str),
        ('speed_1', 'Speed over ground in knots', float),
        ('units_1', 'Units', str),
        ('speed_2', 'Speed over ground in kilometers/hour', float),
        ('units_2', 'Units', str),
        # ('mode', 'Mode', str), NMEA V 3.00
    )

    @property
    def is_valid(self):
        return True

    def __init__(self):
        super(VTGSentence, self).__init__()


class Parser(object):
    parsers = {
        GGASentence.sentence_name: GGASentence,
        GLLSentence.sentence_name: GLLSentence,
        RMCSentence.sentence_name: RMCSentence,
        VTGSentence.sentence_name: VTGSentence,
    }

    def _get_parser(self, name):
        parser = Parser.parsers.get(name.upper())

        if parser:
            return parser()

        return None

    def parse(self, data):
        if not data:
            raise ParseException('Can\'t parse empty data.')

        if data[0] == u'$':
            data = data[1:]

        if data[0:2] == u'GP':
            data = data[2:]

        sentence = data[0:3]
        parser = self._get_parser(sentence)

        if not parser:
            raise ParseException('Can\'t find parser for sentence: %s' % sentence)

        return parser.parse(data[4:])

if __name__ == '__main__':
    parser = Parser()

    sentence = parser.parse('$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47')
    print(sentence.to_dict())

    sentence = parser.parse('$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D')
    print(sentence.to_dict())

    sentence = parser.parse('$GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M, , , ,0000*18')
    print(sentence.to_dict())

    sentence = parser.parse('$GPGLL,3723.2475,N,12158.3416,W,161229.487,A*41')
    print(sentence.to_dict())

    sentence = parser.parse('$GPVTG,309.62,T, ,M,0.13,N,0.2,K*23')
    print(sentence.to_dict())

    sentence = parser.parse('$GPRMC,161229.487,A,3723.2475,N,12158.3416,W,0.13,309.62,120508,*10')
    print(sentence.to_dict())
