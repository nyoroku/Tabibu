# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-04-13 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inpatient', '0008_auto_20200406_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='reason',
            field=models.TextField(default=b'Reason for admission'),
        ),
    ]
