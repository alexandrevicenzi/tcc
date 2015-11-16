# -*- coding: utf-8 -*-

import dateutil.parser
import json
import paho.mqtt.client as mqtt
import traceback

from collections import namedtuple
from datetime import date, time
from pymongo import MongoClient

import nmea
import notify

Auth = namedtuple('Auth', ['user', 'pwd'])

MQTT_ADDRESS = 'tcc.alexandrevicenzi.com'
MQTT_PORT = 1883
MQTT_AUTH = Auth('guest', 'guest')
MQTT_TIMEOUT = 120

MONGO_ADDRESS = 'tcc.alexandrevicenzi.com'
MONGO_PORT = 27017


def signal_quality(db):
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms706828(v=vs.85).aspx
    if db >= -50:
        return 100
    if db <= -100:
        return 0
    return 2 * (db + 100)


def extract_gps_data(data):
    if data.is_valid:
        if data.sentence_name == 'GGA' or data.sentence_name == 'GLL':
            return {
                'latitude': data.latitude_degree,
                'longitude': data.longitude_degree,
                'is_valid': True,
            }
        elif data.sentence_name == 'RMC':
            return {
                'latitude': data.latitude_degree,
                'longitude': data.longitude_degree,
                'velocity': data.speed_km_h,
                'is_valid': True,
            }
        elif data.sentence_name == 'VTG':
            return {
                'velocity': data.speed_2,
                'is_valid': True,
            }

    return {'is_valid': False}


def to_mongo_type(d):
    def convert(value):
        if isinstance(value, time):
            return value.strftime('%H:%M:%S')
        if isinstance(value, date):
            return value.strftime('%d/%m/%Y')
        elif type(value) == dict:
            return {k: convert(v) for k, v in value.items()}
        else:
            return value

    return convert(d)


class Morudall(mqtt.Client):

    def __init__(self, debug):
        super(Morudall, self).__init__()
        self.on_connect = self._on_connect
        self.on_message = self._on_message
        self._debug = debug
        self._notify = notify.Notify()

        uri = 'mongodb://%s:%d/' % (MONGO_ADDRESS, MONGO_PORT)
        mc = MongoClient(uri)
        self._db = mc['morudall']

    def _on_connect(self, client, userdata, flags, rc):
        print('Connected with result code: %s' % str(rc))
        self.subscribe('/accesspoint')
        self.subscribe('/gpslocation')

    def _on_message(self, client, userdata, msg):
        print('Got message from: %s' % msg.topic)

        if msg.topic == '/accesspoint':
            try:
                payload = json.loads(msg.payload)
                device_id = payload['id']
                dt = dateutil.parser.parse(payload['ts'])
                bssid, ssid, rssi, authmode, channel = payload['data'].split(',')

                data = {
                    'device': device_id,
                    'time': dt,
                    'ap': {
                        'bssid': bssid,
                        'ssid': ssid,
                        'rssi': rssi,
                        'authmode': authmode,
                        'channel': channel,
                        'signal_quality': signal_quality(rssi)
                    }
                }

                self._save_ap_data(data)
            except:
                traceback.print_exc()

        if msg.topic == '/gpslocation':
            try:
                payload = json.loads(msg.payload)
                device_id = payload['id']
                dt = dateutil.parser.parse(payload['ts'])
                nmea_sentece = payload['data']

                try:
                    sentence = nmea.Parser().parse(nmea_sentece)
                    extra = extract_gps_data(sentence)
                    gps_data = sentence.to_dict()
                except:
                    traceback.print_exc()
                    gps_data = None
                    extra = {}

                data = {
                    'device': device_id,
                    'time': dt,
                    'raw_gps': nmea_sentece,
                    'gps_data': gps_data
                }

                data.update(extra)

                self._save_gps_data(data)
            except:
                traceback.print_exc()

    def _save_ap_data(self, data):
        self._notify.send('near', data['device'], 'bus_near')

        if self._debug:
            print(data)
        else:
            return self._db.ap_data.insert_one(to_mongo_type(data)).inserted_id

    def _save_gps_data(self, data):
        is_valid = data.get('gps_data', {}).get('is_valid', False)

        if is_valid:
            lat = data.get('gps_data', {}).get('latitude_degree')
            lon = data.get('gps_data', {}).get('longitude_degree')

            if lat and lon:
                sse_data = '%s,%f,%f' % (data['device'], lat, lon)
                self._notify.send('position', sse_data, 'bus_position')

        if self._debug:
            print(data)
        else:
            return self._db.gps_data.insert_one(to_mongo_type(data)).inserted_id

    def connect(self):
        self.username_pw_set(MQTT_AUTH.user, MQTT_AUTH.pwd)
        super(Morudall, self).connect(MQTT_ADDRESS, MQTT_PORT, MQTT_TIMEOUT)


def loop(debug=False):
    m = Morudall(debug)
    m.connect()
    m.loop_forever()

if __name__ == '__main__':
    import sys
    loop('--debug' in sys.argv)
