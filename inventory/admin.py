from django.contrib import admin

# Register your models here.

from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ()
    search_fields = ()
admin.site.register(Item, ItemAdmin)