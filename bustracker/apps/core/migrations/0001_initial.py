# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('ap_model', models.CharField(max_length=250, null=True, verbose_name='Modelo', blank=True)),
                ('bssid', models.CharField(max_length=17, verbose_name='BSSID')),
                ('essid', models.CharField(max_length=17, null=True, verbose_name='ESSID', blank=True)),
                ('ssid', models.CharField(max_length=17, verbose_name='SSID')),
                ('password', models.CharField(max_length=250, verbose_name='Senha')),
                ('frequency', models.FloatField(help_text='Em GHz. Ex: "2.462"', verbose_name='Frequ\xeancia')),
                ('tx_power', models.IntegerField(help_text='Em dBm. Ex: "15"', null=True, verbose_name='TX Power', blank=True)),
                ('ieee_802_11_a', models.BooleanField(default=True, verbose_name='802.11a')),
                ('ieee_802_11_b', models.BooleanField(default=True, verbose_name='802.11b')),
                ('ieee_802_11_g', models.BooleanField(default=True, verbose_name='802.11g')),
                ('ieee_802_11_n', models.BooleanField(default=True, verbose_name='802.11n')),
            ],
            options={
                'verbose_name': 'Access Point',
                'verbose_name_plural': 'Access Points',
            },
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('details', models.TextField(max_length=250, null=True, verbose_name='Detalhes', blank=True)),
                ('device_id', models.CharField(help_text=b'MAC Address.', max_length=17, verbose_name='ID do Dispositivo')),
            ],
            options={
                'verbose_name': '\xd4nibus',
                'verbose_name_plural': '\xd4nibus',
            },
        ),
        migrations.CreateModel(
            name='BusRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('details', models.TextField(max_length=250, null=True, verbose_name='Detalhes', blank=True)),
                ('code', models.IntegerField(verbose_name='C\xf3digo')),
            ],
            options={
                'verbose_name': 'Rota',
                'verbose_name_plural': 'Rotas',
            },
        ),
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('details', models.TextField(max_length=250, null=True, verbose_name='Detalhes', blank=True)),
                ('latitude', models.DecimalField(verbose_name='Latitude', max_digits=12, decimal_places=8)),
                ('longitude', models.DecimalField(verbose_name='Longitude', max_digits=12, decimal_places=8)),
                ('stop_type', models.CharField(default=b'bus-station', max_length=15, verbose_name='Tipo da Parada', choices=[(b'bus-stop', 'Ponto'), (b'bus-station', 'Terminal'), (b'garage', 'Garagem')])),
                ('aps', models.ManyToManyField(related_name='ap_set', verbose_name='APs do Terminal (+)', to='core.AccessPoint', blank=True)),
            ],
            options={
                'verbose_name': 'Ponto de Parada',
                'verbose_name_plural': 'Pontos de Parada',
            },
        ),
        migrations.AddField(
            model_name='busroute',
            name='from_stop',
            field=models.ForeignKey(related_name='from_set', verbose_name='Terminal de Sa\xedda', to='core.BusStop'),
        ),
        migrations.AddField(
            model_name='busroute',
            name='stops',
            field=models.ManyToManyField(related_name='stops_set', verbose_name='Terminais de Parada (+)', to='core.BusStop', blank=True),
        ),
        migrations.AddField(
            model_name='busroute',
            name='to_stop',
            field=models.ForeignKey(related_name='to_set', verbose_name='Terminal de Chegada', to='core.BusStop'),
        ),
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(related_name='bus_set', verbose_name='Rota', to='core.BusRoute'),
        ),
    ]
