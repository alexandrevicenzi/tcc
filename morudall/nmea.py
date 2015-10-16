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

from datetime import time


class ParseException(Exception):
    pass


class UTCTimeParser(object):
    '''
        Convert string UTC Time into datetime.time.
        It must follow the format hhmmss (161229) or hhmmss.sss (161229.487).
    '''

    def __new__(cls, value):
        try:
            if len(value) > 6:
                return time(int(value[0:2]), int(value[2:4]), int(value[4:6]), int(value[7:10]))
            else:
                return time(int(value[0:2]), int(value[2:4]), int(value[4:6]))
        except:
            raise ParseException('Can\'t parse value into UTC Time: %s' % value)


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

    def to_dict(self):
        d = {key: self.__dict__[key] for key, _, _ in self.fields}
        d['sentence'] = self.sentence_name
        return d


class GGASentence(Sentence):
    sentence_name = 'GGA'
    sentence_description = 'Global Positioning System Fix Data'
    fields = (
        ('utc_time', 'UTC Time', UTCTimeParser),
        ('latitude', 'Latitude', float),
        ('ns_indicator', 'N/S Indicator', str),
        ('longitude', 'Longitude', float),
        ('ew_indicator', 'E/W Indicator', str),
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


class GLLSentence(Sentence):
    sentence_name = 'GLL'
    sentence_description = 'Geographic Position – Latitude/Longitude'
    fields = (
        ('latitude', 'Latitude', float),
        ('ns_indicator', 'N/S Indicator', str),
        ('longitude', 'Longitude', float),
        ('ew_indicator', 'E/W Indicator', str),
        ('utc_time', 'UTC Time', UTCTimeParser),
        ('status', 'Status', str),
        # ('mode', 'Mode', str), NMEA V 3.00
    )

    def __init__(self):
        super(GLLSentence, self).__init__()


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

    def __init__(self):
        super(VTGSentence, self).__init__()


class Parser(object):
    parsers = {
        GGASentence.sentence_name: GGASentence,
        GLLSentence.sentence_name: GLLSentence,
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
    sentence = Parser().parse(u'$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47')
    print(sentence.to_dict())

    sentence = Parser().parse(u'$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D')
    print(sentence.to_dict())

    sentence = Parser().parse(u'$GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M, , , ,0000*18')
    print(sentence.to_dict())

    sentence = Parser().parse(u'$GPGLL,3723.2475,N,12158.3416,W,161229.487,A*41')
    print(sentence.to_dict())

    sentence = Parser().parse(u'$GPVTG,309.62,T, ,M,0.13,N,0.2,K*23')
    print(sentence.to_dict())
