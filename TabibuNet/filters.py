from django.contrib.auth.models import User
from .models import Patient
from dal import autocomplete
import django_filters

from smart_selects.db_fields import ChainedForeignKey


class PatientFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = ['phone', 'id', 'first_name']



