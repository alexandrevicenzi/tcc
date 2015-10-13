# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151010_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busroute',
            name='terminals',
            field=models.ManyToManyField(related_name='route_set', verbose_name='Terminais de Parada (+)', to='core.BusTerminal', blank=True),
        ),
    ]
