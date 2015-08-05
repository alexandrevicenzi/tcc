# -*- coding: utf-8 -*-

from django.db import models


class BusTerminal(models.Model):
    ''' Terminal de ônibus. '''
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)


class BusRoute(models.Model):
    ''' Linha de ônibus. '''
    is_active = models.BooleanField(default=True)
    code = models.IntegerField()
    route = models.CharField(max_length=100)
    details = models.CharField(max_length=250)
    terminal = models.ForeignKey(BusTerminal, related_name='route_set')


class Bus(models.Model):
    ''' Ônibus da frota. '''
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=10)
    capacity = models.IntegerField(default=0)
    route = models.ForeignKey(BusRoute, related_name='bus_set')
