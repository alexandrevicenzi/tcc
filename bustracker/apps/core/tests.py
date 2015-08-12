# -*- coding: utf-8 -*-

from django.test import TestCase

from .models import BusTerminal


class TestModels(TestCase):

    def setUp(self):
        pass

    def test_insert_bus_terminal(self):
        BusTerminal.objects.create(name='TERMINAL PROEB',
                                   slug='PROEB',
                                   latitude=-26.8964962,
                                   longitude=-49.1063695)

        terminal = BusTerminal.objects.get(pk=1)
        self.assertEquals(terminal.slug, 'PROEB')
