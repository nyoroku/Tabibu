from django.contrib import admin
from .models import Ward, Admission, Bed


class BedAdmin(admin.ModelAdmin):
    list_filter = ('ward', 'name')
    list_display = ('name', 'ward')
    search_fields = ('ward', 'name')
admin.site.register(Bed, BedAdmin)


class WardAdmin(admin.ModelAdmin):
    list_filter = ('type', 'name')
    list_display = ('type', 'name')
    search_fields = ('type', 'name')
admin.site.register(Ward, WardAdmin)


class AdmissionAdmin(admin.ModelAdmin):
    list_filter = ('patient', 'bed', 'admission_date', 'discharge_date', 'status')
    list_display = ('patient', 'bed', 'admission_date', 'discharge_date', 'status')
    search_fields = ('patient', 'bed', 'admission_date', 'discharge_date', 'status')
admin.site.register(Admission, AdmissionAdmin)
