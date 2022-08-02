from .models import Admission, Ward, Bed, Obstetrics, Medtest, Patient, Medication
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, When, Value, Case, PositiveSmallIntegerField
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django_ajax.decorators import ajax
from .forms import AdmissionAddForm, AdmissionEditForm, TestAddForm, ObsAddForm, PrescriptionFormSet
from django.utils.timezone import datetime
from  datetime import date


def add_admission(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        admission_form = AdmissionAddForm(data=request.POST)
        if admission_form.is_valid():
            new_admission = admission_form.save(commit=False)
            new_admission.patient = patient
            new_admission.save()
            return HttpResponseRedirect(patient.get_absolute_url())
    else:
        admission_form = AdmissionAddForm()
    return render(request, 'inpatient/admission.html', {'admission_form': admission_form, 'patient': patient})


class AdmissionListView(SuccessMessageMixin, ListView):
    model = Admission
    template_name = 'inpatient/admission_list.html'
    paginate_by = 5


def admission_detail(request,year,month,day, admission):
    admission = get_object_or_404(Admission, slug=admission)
    tests = Medtest.objects.filter(admission=admission)[:3]
    obs = Obstetrics.objects.filter(admission=admission)
    prescriptions = Medication.objects.filter(admission=admission)
    return render(request, 'inpatient/admission_detail.html', {'admission': admission, 'prescriptions': prescriptions, 'tests': tests, 'obs': obs})


def edit_admission(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)
    if request.method == 'POST':
        admission_form = AdmissionEditForm(instance=admission, data=request.POST, files=request.FILES)
        if admission_form.is_valid():
            admission = admission_form.save(commit=False)
            admission.save()
            messages.success(request, 'Admission Status Updated')
            return HttpResponseRedirect(admission.get_absolute_url())
        else:
            messages.error(request, 'There was a problem when updating profile')
    else:

        admission_form = AdmissionEditForm(instance=admission)
    return render(request, 'inpatient/admission_update.html', {'admission_form': admission_form, 'admission': admission})


def add_test(request, admission_id):
    admission = get_object_or_404(Admission, pk=admission_id)
    if request.method == 'POST':
        test_form = TestAddForm(data=request.POST)
        if test_form.is_valid():
            new_test = test_form.save(commit=False)
            new_test.admission = admission
            new_test.save()
            messages.success(request, 'Test Updated')
            return HttpResponseRedirect(admission.get_absolute_url())
    else:
        test_form = TestAddForm()
    return render(request, 'patients/test.html', {'test_form': test_form, 'admission': admission})


def add_obs(request, admission_id):
    admission = get_object_or_404(Admission, pk=admission_id)
    if request.method == 'POST':
        test_form = ObsAddForm(data=request.POST)
        if test_form.is_valid():
            new_test = test_form.save(commit=False)
            new_test.admission = admission
            new_test.save()
            messages.success(request, 'Test Updated')
            return HttpResponseRedirect(admission.get_absolute_url())
    else:
        test_form = ObsAddForm()
    return render(request, 'patients/obtest.html', {'test_form': test_form, 'admission': admission})


class AdmissionPrescriptionUpdateView(TemplateResponseMixin, View):
    template_name = 'patients/formset.html'
    property = None

    def get_formset(self, data=None):
        return PrescriptionFormSet(instance=self.admission, data=data)

    def dispatch(self, request, pk):
        self.admission = get_object_or_404(Admission, id=pk)
        return super(AdmissionPrescriptionUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'visit': self.admission, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if request.method == 'POST':
            formset = PrescriptionFormSet(request.POST, request.FILES, instance=self.admission)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Medication Updated')
            return HttpResponseRedirect(self.admission.get_absolute_url())
        else:
            messages.error(request, 'There was a problem updating medication')
        return self.render_to_response({'admission': self.admission, 'formset': formset})