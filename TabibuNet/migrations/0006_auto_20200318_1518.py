# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-03-18 12:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TabibuNet', '0005_auto_20200318_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 18, 15, 18, 52, 645000)),
        ),
    ]
