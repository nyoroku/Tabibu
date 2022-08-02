from django.db import models
from TabibuNet.models import Visit
from inventory.models import Item
from django.core.urlresolvers import reverse
from decimal import Decimal


class Invoice(models.Model):
    visit = models.ForeignKey(Visit)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200)
    item = models.ForeignKey(Item)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Invoice {}'.format(self.id)

    def get_cost(self):
        return self.item.price * self.quantity











