from django import forms
from django.forms import inlineformset_factory
from .models import Patient, MedicalInfo, Visit, Prescription, MedicalTest, Obstetrics, LabTest, Test, Medication
from invoice.models import Invoice
from dal import autocomplete
MedicalInfoFormSet = inlineformset_factory(Patient, MedicalInfo, fields=['blood_type', 'height', 'weight', 'comments',
                                                                         'blood_pressure', 'asthma', 'stroke',
                                                                         'diabetes', 'chronic_disease', 'allergy', 'alzheimer' ], can_delete=True, extra=0
                                           )


class InfoEditForm(forms.ModelForm):
    class Meta:
        model = MedicalInfo
        fields = ('blood_type','blood_pressure', 'height', 'weight',
                   'asthma', 'stroke',
                  'diabetes', 'chronic_disease', 'allergy', 'alzheimer','comments')


class VisitAddForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ()


class VisitEditForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ('chief_complaints', )

MedicationFormSet = inlineformset_factory(Prescription, Medication, fields=['medication', 'strength', 'instruction', 'refill', 'active'], extra=2, can_delete=True)


class TestAddForm(forms.ModelForm):
    class Meta:
        model = MedicalTest
        fields = ('history', 'examination', 'diagnosis', 'ddx')


class ObsAddForm(forms.ModelForm):
    class Meta:
        model = Obstetrics
        fields = ('name', 'examination', 'diagnosis')


InvoiceFormSet = inlineformset_factory(Visit, Invoice, fields=['item', 'quantity'], extra=2, can_delete=True)


class LabForm(forms.ModelForm):
    medical_test = forms.ModelChoiceField(
        queryset=Test.objects.all(),
        widget=autocomplete.ModelSelect2(url='TabibuNet:test-autocomplete')
    )

    class Meta:

        model = LabTest
        fields = ('medical_test', )


class LabEditForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ('examination', 'diagnosis')
