# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Bill
# Register your models here.


class BillAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    list_display = ('status', )
    search_fields = ('status', )
admin.site.register(Bill, BillAdmin)
