# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-06 01:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0004_auto_20181003_0231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boleto',
            name='nome_empresa',
        ),
    ]