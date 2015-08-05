# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=10)),
                ('capacity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BusRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.IntegerField()),
                ('route', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='BusTerminal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=10)),
                ('latitude', models.DecimalField(max_digits=8, decimal_places=5)),
                ('longitude', models.DecimalField(max_digits=8, decimal_places=5)),
            ],
        ),
        migrations.AddField(
            model_name='busroute',
            name='terminal',
            field=models.ForeignKey(related_name='route_set', to='core.BusTerminal'),
        ),
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(related_name='bus_set', to='core.BusRoute'),
        ),
    ]
