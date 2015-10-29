# -*- coding: utf-8 -*-

from pymongo import MongoClient

MONGO_ADDRESS = 'tcc.alexandrevicenzi.com'
MONGO_PORT = 27017


class DB(object):

    def __init__(self):
        uri = 'mongodb://%s:%d/' % (MONGO_ADDRESS, MONGO_PORT)
        mc = MongoClient(uri)
        self._db = mc['morudall']


def get_last_ap_data(device_id):
    return None


def get_last_gps_data(device_id, sentence):
    return None


def get_avg_velocity(device_id, interval=0):
    return 0
