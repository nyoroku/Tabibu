from django.db import models
from TabibuNet.models import Visit
from inventory.models import Item
from django.core.urlresolvers import reverse
from TabibuNet.models import Visit, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
from django_fsm import transition, FSMIntegerField
from datetime import datetime, date


class Appointment(models.Model):
    visit = models.OneToOneField(Visit, related_name='appointments')
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    provider = models.ForeignKey(User, related_name='appointments')




