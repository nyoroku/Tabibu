# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-08-06 17:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TabibuNet', '0004_auto_20200806_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 6, 20, 48, 46, 183000)),
        ),
    ]
