# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-03-18 10:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TabibuNet', '0003_auto_20200318_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 18, 13, 59, 43, 803000)),
        ),
    ]
