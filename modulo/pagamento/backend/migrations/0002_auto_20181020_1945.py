# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-10-20 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produtos',
            name='availableToSell',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='category',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='description',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='imageURLs',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='name',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='ownerGroup',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='quantityInStock',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='type_produto',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='value',
        ),
        migrations.RemoveField(
            model_name='produtos',
            name='weight',
        ),
        migrations.AlterField(
            model_name='produtos',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]