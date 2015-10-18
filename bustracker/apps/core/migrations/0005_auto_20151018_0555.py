# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151013_0332'),
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
        ),
        migrations.AddField(
            model_name='busterminal',
            name='aps',
            field=models.ManyToManyField(related_name='ap_set', verbose_name='APs do Terminal (+)', to='core.AccessPoint', blank=True),
        ),
    ]
