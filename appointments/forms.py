from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import Appointment
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField
from dal import autocomplete


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('date', 'start_time', 'end_time',)