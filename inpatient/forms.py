from .models import Admission, Medtest, Obstetrics, Medication
from django import forms
from django.forms import inlineformset_factory


class AdmissionAddForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ('bed', 'reason', 'status')


class AdmissionEditForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ('status', )


class TestAddForm(forms.ModelForm):
    class Meta:
        model = Medtest
        fields = ('name', 'examination', 'diagnosis')


class ObsAddForm(forms.ModelForm):
    class Meta:
        model = Obstetrics
        fields = ('name', 'examination', 'diagnosis')

PrescriptionFormSet = inlineformset_factory(Admission, Medication, fields=['medication', 'strength', 'instruction', 'refill', 'active' ], extra=2, can_delete=True)