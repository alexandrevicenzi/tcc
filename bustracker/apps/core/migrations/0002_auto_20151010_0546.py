# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='details',
            field=models.TextField(max_length=250, null=True, verbose_name='Detalhes', blank=True),
        ),
        migrations.AlterField(
            model_name='busroute',
            name='details',
            field=models.TextField(max_length=250, null=True, verbose_name='Detalhes', blank=True),
        ),
        migrations.AlterField(
            model_name='busterminal',
            name='details',
            field=models.TextField(max_length=250, null=True, verbose_name='Detalhes', blank=True),
        ),
    ]
