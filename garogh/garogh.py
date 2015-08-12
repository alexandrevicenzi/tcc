# -*- coding: utf-8 -*-

from collections import namedtuple
from datetime import datetime
from pymongo import MongoClient, DESCENDING


Location = namedtuple('Location', ['id', 'slug', 'latitude', 'longitude', 'timestamp'])


class Locator(object):
    '''
        MondoDB interface to interact
        with positions statistics.
    '''

    def __init__(self, uri='mongodb://localhost:27017/', db=None):
        if db is None:
            self._db_name = 'locator'
        else:
            self._db_name = db

        self._client = MongoClient(uri)
        self._db = self._client[self._db_name]

    def get_lastest_location(self, slug):
        loc = self._db.location.find_one({'$query': {'slug': slug}, '$orderby': {'date': DESCENDING}})

        if loc:
            return Location(loc['_id'], loc['slug'], loc['lat'], loc['lon'], loc['date'])

        return None

    def add_location(self, slug, latitude, longitude, timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow()

        loc = {
            'slug': slug,
            'lat': latitude,
            'lon': longitude,
            'date': timestamp
        }

        return self._db.location.insert_one(loc).inserted_id

    def drop_database(self):
        self._client.drop_database(self._db_name)
