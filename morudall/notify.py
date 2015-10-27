# -*- coding: utf-8 -*-

import redis
import json


class Notify:
    '''
        Wrapper for Django SSE.
        This can notify Django SSE outside an Django App.
    '''
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        pool = redis.ConnectionPool(
            db=db,
            password=password,
            host=host,
            port=port
        )

        self.connection = redis.Redis(connection_pool=pool)
        self.pubsub = self.connection.pubsub()

    def send(self, event, data, channel):
        '''
        Send an event to a particular channel.

        Arguments:
          event     the name of the event to be sent.
          data      data (dict) to be sent along with the event.
          channel   the name of the channel to send event to.
        '''
        self.connection.publish(channel, json.dumps([event, data]))

    def subscribe(self, channel):
        '''
            Subscribe to a channel.

        Arguments:
          channel   the name of the channel to send event to.
        '''
        self.pubsub.subscribe(channel)

    def listen(self):
        '''
        Receive an event.

        Returns:
          event     the name of the event to be sent.
          data      data (dict) to be sent along with the event.
        '''
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                event, data = json.loads(message['data'].decode('utf-8'))
                yield event, data


if __name__ == '__main__':
    notify = Notify()
    notify.send('near', {'device': 'device_id'}, 'bus_near')
