# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-25 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20181025_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrinho',
            name='total_carrinho',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='carrinho',
            name='total_frete',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='produtos_no_carrinho',
            name='valor_unitario',
            field=models.FloatField(default=-1),
        ),
    ]
