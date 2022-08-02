from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from datetime import datetime
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from TabibuNet.models import Patient


class Item(models.Model):
    name = models.CharField(max_length=255)
    measurement = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name















