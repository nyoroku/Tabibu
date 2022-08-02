from django.contrib import admin
from .models import Insurance, Visit, Provider, Test, User, Prescription
from home.models import Registration
import csv
import datetime
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin




class InsuranceAdmin(admin.ModelAdmin):
    list_filter = ('added', 'company',  'description')
    list_display = ('company', 'added')
    search_fields = ('added', 'company',  'description')
admin.site.register(Insurance, InsuranceAdmin)


class VisitAdmin(admin.ModelAdmin):
    list_filter = ('patient',)
    list_display = ('patient', 'status')
    search_fields = ('patient', 'status')
admin.site.register(Visit, VisitAdmin)


class UsersAdmin(UserAdmin):
    list_filter = ('username',)
    list_display = ('username', )
    search_fields = ('username', )
UsersAdmin.fieldsets += ('Choices', {'fields': ('is_lab', 'is_nurse', 'is_provider', 'is_dental', 'is_pharmacy')}),
admin.site.register(User, UsersAdmin)


class TestAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', )
    search_fields = ('name', )
admin.site.register(Test, TestAdmin)


class PrescriptionAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('status',)
    search_fields = ('status', )
admin.site.register(Prescription, PrescriptionAdmin)

