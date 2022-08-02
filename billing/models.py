from django.db import models
from TabibuNet.models import Visit, LabTest
from inventory.models import Item
from django.core.urlresolvers import reverse
from TabibuNet.models import Visit
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
from django_fsm import transition, FSMIntegerField
from datetime import datetime, date
from coupons.models import Coupon


class Bill(models.Model):
    unpaid = 1
    paid = 2

    STATUS = (
        ('unpaid', 'UNPAID'),
        ('paid', 'PAID'),

    )
    visit = models.OneToOneField(Visit)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = FSMIntegerField(choices=STATUS, default=unpaid)
    slug = models.SlugField(max_length=200)
    coupon = models.OneToOneField(Coupon, related_name='coupon', null=True, blank=True)

    @transition(field=status, source=unpaid, target=paid)
    def confirm_payment(self):
        pass


    @receiver(post_save, sender=Visit)
    def create_visit_bill(sender, instance, created, **kwargs):
        if created:
            Bill.objects.create(visit=instance)

    @receiver(post_save, sender=Visit)
    def save_visit_bill(sender, instance, **kwargs):
        instance.bill.save()

    def save(self, *args, **kwargs):
        super(Bill, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.visit.patient.first_name)
            self.save()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Bill {}'.format(self.visit.patient.first_name)

    def get_absolute_url(self):
        return reverse('billing:bill', args=[self.visit.pk])

    def total_items(self):
        total = 0
        items = self.billitem_set.all()

        for item in items:
            total += item.item.price * item.quantity
        return total


class BillItem(models.Model):
    bill = models.ForeignKey(Bill)
    item = models.ForeignKey(Item)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.item.price * self.quantity


class LabBill(models.Model):
    unpaid = 1
    paid = 2

    STATUS = (
        ('unpaid', 'UNPAID'),
        ('paid', 'PAID'),


    )
    lab_test = models.OneToOneField(LabTest)
    status = FSMIntegerField(choices=STATUS, default=unpaid)
    created = models.DateTimeField(default=datetime.now())

    @receiver(post_save, sender=LabTest)
    def create_lab_bill(sender, instance, created, **kwargs):
        if created:
            LabBill.objects.create(lab_test=instance)

    @receiver(post_save, sender=LabTest)
    def save_lab_bill(sender, instance, **kwargs):
        instance.labbill.save()

    @transition(field=status, source=unpaid, target=paid)
    def confirm_payment(self):
        pass

















