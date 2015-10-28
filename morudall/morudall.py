# -*- coding: utf-8 -*-

import dateutil.parser
import json
import paho.mqtt.client as mqtt

from collections import namedtuple
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
                        'channel': channel
                    }
                }

                self._save_ap_data(data)
            except Exception as e:
                print(str(e))

        if msg.topic == '/gpslocation':
            try:
                payload = json.loads(msg.payload)
                device_id = payload['id']
                dt = dateutil.parser.parse(payload['ts'])
                nmea_sentece = payload['data']

                try:
                    nmea_parsed = nmea.Parser().parse(nmea_sentece)
                except:
                    nmea_parsed = None

                data = {
                    'device': device_id,
                    'time': dt,
                    'raw_gps': nmea_sentece,
                    'gps_data': nmea_parsed
                }

                self._save_gps_data(data)
            except Exception as e:
                print(str(e))

    def _save_ap_data(self, data):
        self._notify.send('near', data['device_id'], 'bus_near')

        if self._debug:
            print(data)
        else:
            return self._db.ap_data.insert_one(data).inserted_id

    def _save_gps_data(self, data):
        if self._debug:
            print(data)
        else:
            return self._db.gps_data.insert_one(data).inserted_id

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
