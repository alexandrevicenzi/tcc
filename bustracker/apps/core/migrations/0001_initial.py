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
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('details', models.CharField(max_length=250, null=True, verbose_name='Detalhes', blank=True)),
                ('device_id', models.CharField(help_text=b'MAC Address.', max_length=17, verbose_name='ID do Dispositivo')),
            ],
        ),
        migrations.CreateModel(
            name='BusRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('details', models.CharField(max_length=250, null=True, verbose_name='Detalhes', blank=True)),
                ('code', models.IntegerField(verbose_name='C\xf3digo')),
            ],
        ),
        migrations.CreateModel(
            name='BusTerminal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('details', models.CharField(max_length=250, null=True, verbose_name='Detalhes', blank=True)),
                ('latitude', models.DecimalField(verbose_name='Latitude', max_digits=12, decimal_places=8)),
                ('longitude', models.DecimalField(verbose_name='Longitude', max_digits=12, decimal_places=8)),
            ],
        ),
        migrations.AddField(
            model_name='busroute',
            name='from_terminal',
            field=models.ForeignKey(related_name='from_set', verbose_name='Terminal de Sa\xedda', to='core.BusTerminal'),
        ),
        migrations.AddField(
            model_name='busroute',
            name='terminals',
            field=models.OneToOneField(related_name='route_set', verbose_name='Terminais de Parada', to='core.BusTerminal'),
        ),
        migrations.AddField(
            model_name='busroute',
            name='to_terminal',
            field=models.ForeignKey(related_name='to_set', verbose_name='Terminal de Chegada', to='core.BusTerminal'),
        ),
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(related_name='bus_set', verbose_name='Rota', to='core.BusRoute'),
        ),
    ]
