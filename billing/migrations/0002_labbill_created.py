# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-05-20 09:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='labbill',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 20, 12, 23, 40, 70000)),
        ),
    ]
