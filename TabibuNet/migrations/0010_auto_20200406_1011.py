# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-04-06 07:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TabibuNet', '0009_auto_20200406_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 6, 10, 11, 29, 279000)),
        ),
    ]