from django.shortcuts import render, get_object_or_404
from .models import Patient,Prescription, MedicalTest, MedicalInfo, Visit, Obstetrics, LabTest, Test, User
from inpatient.models import Admission
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.core.urlresolvers import reverse_lazy, reverse
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
from .forms import InfoEditForm, VisitAddForm, VisitEditForm, MedicationFormSet, TestAddForm, ObsAddForm, \
     InvoiceFormSet, LabForm, LabEditForm, Medication
from django.utils.timezone import datetime
from datetime import date
from billing.models import Bill
from .filters import PatientFilter
from invoice.models import Invoice
from django_fsm import can_proceed
from dal import autocomplete
from django_fsm_log.models import StateLog
from django.db.models import F





class PatientCreate(SuccessMessageMixin, CreateView):
    model = Patient

    fields = ['first_name', 'last_name', 'gender', 'phone', 'email', 'contact_person', 'married', 'dob', 'location', 'address',
              'insurance']
    template_name = 'patients/patient.html'
    success_url = reverse_lazy('TabibuNet:search_patient')
    success_message = 'Patient Successfully Added'


class PatientListView(SuccessMessageMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    paginate_by = 4


class PatientUpdateView(SuccessMessageMixin, UpdateView):
    model = Patient
    fields = ['first_name', 'last_name', 'gender', 'phone', 'email', 'contact_person', 'married', 'dob', 'location',
              'address',
              'insurance']
    template_name = 'patients/patient.html'
    success_message = 'Successfully Updated'
    success_url = reverse_lazy('TabibuNet:patient_list')


def patient_detail(request,year,month,day, patient):
    patient = get_object_or_404(Patient, slug=patient)
    info = MedicalInfo.objects.filter(patient=patient)
    visits = Visit.objects.filter(patient=patient)
    admissions = Admission.objects.filter(patient=patient)
    return render(request, 'patients/patient_detail.html', {'patient': patient, 'info': info, 'visits': visits, 'admissions': admissions})


def edit(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    info = get_object_or_404(MedicalInfo, patient=patient)
    if request.method == 'POST':
        info_form = InfoEditForm(instance=info, data=request.POST, files=request.FILES)
        if info_form.is_valid():
            info = info_form.save(commit=False)
            info.save()
            messages.success(request, 'Info updated')
            return HttpResponseRedirect(patient.get_absolute_url())
        else:
            messages.error(request, 'There was a problem when updating profile')
    else:

        info_form = InfoEditForm(instance=info)
    return render(request, 'patients/infoedit.html', {'info_form': info_form, 'patient': patient})


def waiting_for_provider(request):
    visits = Visit.objects.filter(status=2)
    total_visits = visits.count()
    paginator = Paginator(visits, 12)
    page = request.GET.get('page')
    try:
        visits = paginator.page(page)
    except PageNotAnInteger:
        visits = paginator.page(1)
    except EmptyPage:
        visits = paginator.page(paginator.num_pages)
    return render(request, 'patients/wait_provider.html', {'visits': visits, 'page': page, 'total_visits': total_visits})


def add_visit(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        visit_form = VisitAddForm(data=request.POST)
        if visit_form.is_valid():
            new_visit = visit_form.save(commit=False)
            new_visit.patient = patient
            new_visit.save()
            new_visit.reception(by=request.user)
            new_visit.save()
            messages.success(request, 'Visit Added')
            return redirect('TabibuNet:visit_list')
    else:
        visit_form = VisitAddForm()
    return render(request, 'patients/visit.html', {'visit_form': visit_form, 'patient': patient})


class VisitListView(SuccessMessageMixin, ListView):

    model = Visit
    template_name = 'patients/visit_list.html'
    paginate_by = 12


def visit_detail(request,year,month,day, visit):
    visit = get_object_or_404(Visit, slug=visit)
    states = StateLog.objects.all().order_by('-timestamp').for_(visit)
    bills = Bill.objects.filter(visit=visit)
    invoices = Invoice.objects.filter(visit=visit)
    tests = MedicalTest.objects.filter(visit=visit)[:3]
    labtests = LabTest.objects.filter(visit=visit)
    prescription = Prescription.objects.get(visit=visit)
    medications = Medication.objects.filter(prescription=prescription)
    return render(request, 'patients/visit_detail.html', {'visit': visit, 'prescription': prescription, 'tests': tests, 'labtests': labtests, 'invoices': invoices,
                                                        'bills': bills, 'states': states, 'medications': medications})


def edit_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    if request.method == 'POST':
        visit_form = VisitEditForm(instance=visit, data=request.POST, files=request.FILES)
        if visit_form.is_valid():
            visit = visit_form.save(commit=False)
            visit.save()
            messages.success(request, 'Visit Status Updated')
            return HttpResponseRedirect(visit.get_absolute_url())
        else:
            messages.error(request, 'There was a problem updating status')
    else:

        visit_form = VisitEditForm(instance=visit)
    return render(request, 'patients/update_visit.html', {'visit_form': visit_form, 'visit': visit})


class PrescriptionMedicationUpdateView(TemplateResponseMixin, View):
    template_name = 'patients/formset.html'
    prescription = None

    def get_formset(self, data=None):
        return MedicationFormSet(instance=self.prescription, data=data)

    def dispatch(self, request, pk):
        self.prescription = get_object_or_404(Prescription, id=pk)
        return super(PrescriptionMedicationUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'visit': self.prescription, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if request.method == 'POST':
            formset = MedicationFormSet(request.POST, request.FILES, instance=self.prescription)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Prescription Updated')
            return HttpResponseRedirect(self.prescription.get_absolute_url())
        else:
            messages.error(request, 'There was a problem updating prescription')
        return self.render_to_response({'visit': self.prescription, 'formset': formset})


def prescription_detail(request, pk):
    visit = Visit.objects.get(pk=pk)
    prescription = Prescription.objects.get(visit=visit)
    medication = Medication.objects.filter(prescription=prescription)
    return render(request, 'patients/presciption_detail.html', {'prescription': prescription, 'visit': visit, 'medication': medication})


def add_test(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    if request.method == 'POST':
        test_form = TestAddForm(data=request.POST)
        if test_form.is_valid():
            new_test = test_form.save(commit=False)
            new_test.visit = visit
            new_test.save()
            messages.success(request, 'Test Updated')
            return HttpResponseRedirect(visit.get_absolute_url())
    else:
        test_form = TestAddForm()
    return render(request, 'patients/test.html', {'test_form': test_form, 'visit': visit})


def add_obs(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    if request.method == 'POST':
        test_form = ObsAddForm(data=request.POST)
        if test_form.is_valid():
            new_test = test_form.save(commit=False)
            new_test.visit = visit
            new_test.save()
            messages.success(request, 'Test Updated')
            return HttpResponseRedirect(visit.get_absolute_url())
    else:
        test_form = ObsAddForm()
    return render(request, 'patients/obtest.html', {'test_form': test_form, 'visit': visit})


def test_detail(request,year,month,day, test):
    test = get_object_or_404(MedicalTest, slug=test)
    return render(request, 'patients/test_detail.html', {'test': test})


def ob_detail(request,year,month,day, ob):
    ob = get_object_or_404(Obstetrics, slug=ob)
    return render(request, 'patients/ob_detail.html', {'ob': ob})


def patient_filter(request):
    f = PatientFilter(request.GET, queryset=Patient.objects.all())
    patient = f.qs
    total_patients = patient.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(f.qs, 3)
    try:
        patient = paginator.page(page)
    except PageNotAnInteger:
        patient = paginator.page(1)
    except EmptyPage:
        patient = paginator.page(paginator.num_pages)

    return render(request, 'patients/patient_search.html', {'filter': f, 'patient': patient, 'total_patients': total_patients})


class VisitInvoiceUpdateView(TemplateResponseMixin, View):
    template_name = 'patients/invoice_formset.html'
    visit = None

    def get_formset(self, data=None):
        return InvoiceFormSet(instance=self.visit, data=data)

    def dispatch(self, request, pk):
        self.visit = get_object_or_404(Visit, id=pk)
        return super(VisitInvoiceUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'visit': self.visit, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if request.method == 'POST':
            formset = InvoiceFormSet(request.POST, request.FILES, instance=self.visit)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Invoice Updated')
            return HttpResponseRedirect(self.visit.get_absolute_url())
        else:
            messages.error(request, 'There was a problem updating invoice')
        return self.render_to_response({'visit': self.visit, 'formset': formset})


class InvoiceListView(SuccessMessageMixin, ListView):
    model = Invoice
    template_name = 'invoice/invoice_list.html'
    paginate_by = 5


def send_to_provider(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)

    visit.waiting_for_provider(by=request.user)
    visit.save()
    messages.success(request, 'Patient waiting to see a clinician')
    return render(request, 'patients/sent_to_provider.html', {'visit': visit})


def provider(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    visit.provider(by=request.user)
    visit.save()
    messages.success(request, 'You are attending to the patient')
    return HttpResponseRedirect(visit.get_absolute_url())


def lab_test(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    if request.method == 'POST':
        test_form = LabForm(data=request.POST)
        if test_form.is_valid():
            new_test = test_form.save(commit=False)
            new_test.visit = visit
            new_test.save()
            visit.send_to_lab(by=request.user)
            visit.save()
            messages.success(request, 'Patient Sent To Lab')
            return render(request, 'patients/sent_to_lab.html', {'visit': visit})

    else:
        test_form = LabForm()
    return render(request, 'patients/test.html', {'test_form': test_form, 'visit': visit})


def provider_to_lab(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    if request.method == 'POST':
        test_form = LabForm(data=request.POST)
        if test_form.is_valid():
            new_test = test_form.save(commit=False)
            new_test.visit = visit
            visit.send_to_lab(by=request.user)
            visit.save()
            new_test.save()

            messages.success(request, 'Patient Sent To Lab')
            return redirect('TabibuNet:waiting_for_provider')

    else:
        test_form = LabForm()
    return render(request, 'patients/test.html', {'test_form': test_form, 'visit': visit})


def waiting_for_lab(request):
    visits = Visit.objects.filter(status=6)
    total_visits = visits.count()
    paginator = Paginator(visits, 12)
    page = request.GET.get('page')
    try:
        visits = paginator.page(page)
    except PageNotAnInteger:
        visits = paginator.page(1)
    except EmptyPage:
        visits = paginator.page(paginator.num_pages)
    return render(request, 'patients/wait_for_lab.html', {'visits': visits, 'page': page, 'total_visits': total_visits})


def wait_for_lab(request):
    tests = LabTest.objects.filter(Q(visit__status=6) & Q(status=1))
    total_tests = tests.count()
    paginator = Paginator(tests, 12)
    page = request.GET.get('page')
    try:
        tests = paginator.page(page)
    except PageNotAnInteger:
        tests = paginator.page(1)
    except EmptyPage:
        tests = paginator.page(paginator.num_pages)
    return render(request, 'patients/waiting_lab.html', {'tests': tests, 'page': page, 'total_tests': total_tests})


def edit_test(request, labtest_id):
    test = get_object_or_404(LabTest, id=labtest_id)
    if request.method == 'POST':
        lab_form = LabEditForm(instance=test, data=request.POST, files=request.FILES)
        if lab_form.is_valid():
            test = lab_form.save(commit=False)
            test.save()
            messages.success(request, 'Test was updated')
            return HttpResponseRedirect(test.get_absolute_url())
        else:
            messages.error(request, 'There was a problem updating test')
    else:

        lab_form = LabEditForm(instance=test)
    return render(request, 'patients/update_lab.html', {'lab_form': lab_form, 'test': test})


def lab(request, labtest_id):
    test = get_object_or_404(LabTest, pk=labtest_id)
    test.lab(by=request.user)
    test.visit.to_lab(by=request.user)
    test.save()
    messages.success(request, 'You are attending to the patient')
    return HttpResponseRedirect(test.get_absolute_url())


class TestAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Test.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


def labtest_detail(request,year,month,day, labtest):
    labtest = get_object_or_404(LabTest, slug=labtest)
    return render(request, 'patients/labtest.html', {'labtest': labtest})


def lab_to_provider(request, labtest_id):
    test = get_object_or_404(LabTest, pk=labtest_id)
    test.lab_to_provider(by=request.user)
    test.visit.to_lab_provider(by=request.user)
    test.save()
    messages.success(request, 'Patient Sent To provider')
    return redirect('TabibuNet:waiting_for_lab')


def provider_to_pharmacy(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    visit.to_pharmacy(by=request.user)
    visit.save()
    messages.success(request, 'Patient Sent To pharmacy')
    return redirect('TabibuNet:waiting_for_provider')


def lab_to_pharmacy(request, labtest_id):
    test = get_object_or_404(LabTest, pk=labtest_id)
    test.lab_to_pharmacy()
    test.save()
    messages.success(request, 'Patient To Pharmacy')
    return redirect('TabibuNet:waiting_for_lab')


def lab_to_close(request, labtest_id):
    test = get_object_or_404(LabTest, pk=labtest_id)
    test.ready_for_close()
    test.save()
    messages.success(request, 'Visit Marked As Ready To Close')
    return redirect('TabibuNet:waiting_for_lab')


def wait_for_pharmacy(request):
    prescriptions = Prescription.objects.filter(Q(visit__status=8) & Q(status=1))
    total_prescriptions = prescriptions.count()
    paginator = Paginator(prescriptions, 12)
    page = request.GET.get('page')
    try:
        prescriptions = paginator.page(page)
    except PageNotAnInteger:
        prescriptions = paginator.page(1)
    except EmptyPage:
        prescriptions = paginator.page(paginator.num_pages)
    return render(request, 'patients/wait_for_pharmacy.html', {'prescriptions': prescriptions, 'page': page, 'total_prescriptions': total_prescriptions})


def pharmacy(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)
    prescription.pharmacy(by=request.user)
    prescription.save()
    visit = prescription.visit
    visit.pharmacy(by=request.user)
    visit.save()
    messages.success(request, 'You are attending to the patient')
    return HttpResponseRedirect(prescription.get_absolute_url())
