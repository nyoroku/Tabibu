# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-05-16 15:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('TabibuNet', '0003_auto_20210516_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 16, 18, 23, 27, 39000)),
        ),
        migrations.AlterField(
            model_name='visit',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(b'Reception', b'Reception'), (b'wait_for_provider', b'Wait_for_provider'), (b'provider', b'Provider'), (b'dental', b'Dental'), (b'wait_for_lab', b'Waiting_for_lab'), (b'lab', b'Lab'), (b'wait_for_pharmacy', b'Wait_for_pharmacy'), (b'pharmacy', b'Pharmacy'), (b'billing', b'Billing'), (b'ready_to_close', b'Ready_to_close'), (b'closed', b'Closed')], default=b'Reception'),
        ),
    ]
