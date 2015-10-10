# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151010_0546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busroute',
            name='terminals',
        ),
        migrations.AddField(
            model_name='busroute',
            name='terminals',
            field=models.ManyToManyField(related_name='route_set', verbose_name='Terminais de Parada', to='core.BusTerminal'),
        ),
    ]
