# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt

from collections import namedtuple


Auth = namedtuple('Auth', ['user', 'pwd'])

MQTT_ADDRESS = 'tcc.alexandrevicenzi.com'
MQTT_PORT = 1883
MQTT_AUTH = Auth('guest', 'guest')
MQTT_TIMEOUT = 120

MONGO_ADDRESS = MQTT_ADDRESS
MONGO_PORT = 27017


def on_connect(client, userdata, flags, rc):
    print('Connected with result code %s' % str(rc))
    client.subscribe('/location')
    client.publish('/location', '@-26.8956032,-49.0794134,124123421,AAA1234')


def on_message(client, userdata, msg):
    if msg.topic == '/location' and msg.payload.startswith('@'):
        lat, lon, ts, slug = msg.payload[1:].split(',')
        client.save_data(client, slug, float(lat), float(lon), ts)


def save_data(client, slug, lat, lon, date):
    client.db.add_location(slug, lat, lon, date)


def log_data(client, slug, lat, lon, date):
    print('latitude %f and longitude %f from %s at %s' % (lat, lon, slug, date))


def loop(debug=False):
    client = mqtt.Client()

    if debug:
        print('Debug mode enabled!')
        client.save_data = log_data
    else:
        from garogh import Locator
        db = Locator('mongodb://%s:%d/' % (MONGO_ADDRESS, MONGO_PORT))
        client.db = db
        client.save_data = save_data

    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_AUTH.user, MQTT_AUTH.pwd)
    client.connect(MQTT_ADDRESS, MQTT_PORT, MQTT_TIMEOUT)

    client.loop_forever()

if __name__ == '__main__':
    import sys
    loop('--debug' in sys.argv)
