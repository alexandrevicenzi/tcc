# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import sys

from collections import namedtuple
from datetime import datetime

Auth = namedtuple('Auth', ['user', 'pwd'])

MQTT_ADDRESS = 'tcc.alexandrevicenzi.com'
MQTT_PORT = 1883
MQTT_AUTH = Auth('guest', 'guest')
MQTT_TIMEOUT = 120

MONGO_ADDRESS = 'tcc.alexandrevicenzi.com'
MONGO_PORT = 27017


def run(device_id):
    mq = mqtt.Client()
    mq.username_pw_set(MQTT_AUTH.user, MQTT_AUTH.pwd)
    mq.connect(MQTT_ADDRESS, MQTT_PORT, MQTT_TIMEOUT)
    #mq.subscribe('/gpslocation', qos=0)

    while True:
        ts = datetime.now().strftime('%Y-%m-%d-T%H:%M:%S-03:00')
        gps = '$GPGGA,233452.000,2654.6882,S,04904.9851,W,2,7,1.14,10.8,M,1.7,M,0000,0000*50'
        data = "{\"data\":\"%s\",\"ts\":\"%s\",\"id\":\"%s\"}" % (gps, ts, device_id)
        mq.publish('/gpslocation', payload=data, qos=0, retain=False)
        print('Sent.')
        time.sleep(30)

if __name__ == '__main__':
    run(sys.argv[1])
