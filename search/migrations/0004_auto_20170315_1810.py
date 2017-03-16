# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20170314_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='lat',
            field=models.DecimalField(decimal_places=10, max_digits=65535),
        ),
        migrations.AlterField(
            model_name='address',
            name='lon',
            field=models.DecimalField(decimal_places=10, max_digits=65535),
        ),
    ]