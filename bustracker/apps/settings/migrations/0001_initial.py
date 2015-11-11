# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_active', models.BooleanField(verbose_name='Ativo', default=True)),
                ('key', models.CharField(verbose_name='Chave', max_length=100)),
                ('value', models.CharField(verbose_name='Valor', max_length=800)),
                ('value_type', models.CharField(max_length=10, verbose_name='Tipo', default='str', choices=[('str', 'String'), ('bool', 'Boolean'), ('float', 'Float'), ('int', 'Integer')])),
            ],
            options={
                'verbose_name': 'Configuração do Sistema',
                'verbose_name_plural': 'Configurações do Sistema',
            },
        ),
    ]
