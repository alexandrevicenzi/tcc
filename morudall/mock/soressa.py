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


def run(device_id):
    mq = mqtt.Client()
    mq.username_pw_set(MQTT_AUTH.user, MQTT_AUTH.pwd)
    mq.connect(MQTT_ADDRESS, MQTT_PORT, MQTT_TIMEOUT)
    #mq.subscribe('/gpslocation', qos=0)

    with open('input.gps', 'r') as f:
        for line in f.readlines():
            line = line[:-1]
            ts = datetime.now().strftime('%Y-%m-%d-T%H:%M:%S')
            data = "{\"data\":\"%s\",\"ts\":\"%s\",\"id\":\"%s\"}" % (line, ts, device_id)
            mq.publish('/gpslocation', payload=data, qos=0, retain=False)
            print('Sent.')
            time.sleep(5)

if __name__ == '__main__':
    run(sys.argv[1])
