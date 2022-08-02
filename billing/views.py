from .models import Bill, BillItem, LabBill
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
from .forms import BillAddForm, BillIForm, InvoiceFormSet, CouponApplyForm
from django.utils.timezone import datetime
from  datetime import date
from TabibuNet.models import Visit
from coupons.models import Coupon



def add_bill(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    if request.method == 'POST':
        bill_form = BillAddForm(data=request.POST)
        if bill_form.is_valid():
            new_bill = bill_form.save(commit=False)
            new_bill.visit = visit
            new_bill.save()
            return HttpResponseRedirect(visit.get_absolute_url())
    else:
        bill_form = BillAddForm()
    return render(request, 'billing/billing.html', {'bill_form': bill_form, 'visit': visit})


def bill_detail(request,year,month,day, bill):
    bill = get_object_or_404(Bill, slug=bill)
    return render(request, 'billing/billing_detail.html', {'bill': bill})


def get_bill(request, pk):
    coupon_add = CouponApplyForm()
    visit = Visit.objects.get(pk=pk)
    bill = Bill.objects.get(visit=visit)
    bill_item = BillItem.objects.filter(bill=bill)
    return render(request, 'billing/billing_detail.html', {'bill': bill, 'visit': visit, 'bill_item': bill_item,
                                                           'coupon_apply': coupon_add})


def bill_update(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    bill = get_object_or_404(Bill, visit=visit)
    if request.method == 'POST':
        bill_form = BillIForm(instance=bill, data=request.POST, files=request.FILES)
        if bill_form.is_valid():
            bill = bill_form.save(commit=False)
            bill.save()
            messages.success(request, 'Bill updated')
            return HttpResponseRedirect(bill.get_absolute_url())
        else:
            messages.error(request, 'There was a problem when updating profile')
    else:

        bill_form = BillIForm(instance=bill)
    return render(request, 'billing/bill_update.html', {'bill_form': bill_form, 'visit': visit})


class BillItemUpdateView(TemplateResponseMixin, View):
    template_name = 'billing/invoice_formset.html'
    bill = None

    def get_formset(self, data=None):
        return InvoiceFormSet(instance=self.bill, data=data)

    def dispatch(self, request, pk):
        self.bill = get_object_or_404(Bill, id=pk)
        return super(BillItemUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'bill': self.bill, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if request.method == 'POST':
            formset = InvoiceFormSet(request.POST, request.FILES, instance=self.bill)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Invoice Updated')
            return HttpResponseRedirect(self.bill.get_absolute_url())
        else:
            messages.error(request, 'There was a problem updating Invoice')
        return self.render_to_response({'bill': self.bill, 'formset': formset})


def lab_bills(request):
    bills = LabBill.objects.filter(status=1).order_by('-created')
    total_bills = bills.count()
    paginator = Paginator(bills, 12)
    page = request.GET.get('page')
    try:
        bills = paginator.page(page)
    except PageNotAnInteger:
        bills = paginator.page(1)
    except EmptyPage:
        bills = paginator.page(paginator.num_pages)
    return render(request, 'billing/all_bills.html', {'bills': bills, 'page': page, 'total_bills': total_bills})


def confirm_payment(request, labbill_id):
    bill = get_object_or_404(LabBill, pk=labbill_id)
    bill.confirm_payment()
    bill.save()
    messages.success(request, 'Payment Confirmed')
    return render(request, 'billing/bill_confirmed.html', {'bill': bill})


def confirm_pay(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    bill.confirm_payment()
    bill.save()
    messages.success(request, 'Payment Confirmed')
    return redirect('billing:bills')


def coupon_apply(request, bill_id):

    bill = get_object_or_404(Bill, pk=bill_id)
    if request.method == 'POST':
        bill_form = CouponApplyForm(instance=bill, data=request.POST, files=request.FILES)
        if bill_form.is_valid():
            coupon = bill_form.cleaned_data.get('coupon')
            coupon_code = Coupon(coupon=coupon)
            coupon_code.save()
            bill = bill_form.save(commit=False)
            bill.save()
            messages.success(request, 'Coupon applied')
            return HttpResponseRedirect(bill.get_absolute_url())
        else:
            messages.error(request, 'There was a problem applying coupon')

    return HttpResponseRedirect(bill.get_absolute_url())


def coupon_appl(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    bill = get_object_or_404(Bill, coupon=coupon)
    if request.method == 'POST':
        bill_form = CouponApplyForm(instance=bill, data=request.POST, files=request.FILES)
        if bill_form.is_valid():
            bill = bill_form.save(commit=False)
            bill.save()
            messages.success(request, 'Coupon was Applied')
            return HttpResponseRedirect(bill.get_absolute_url())
        else:
            messages.error(request, 'There was a problem when updating coupon')
    else:

        bill_form = CouponApplyForm(instance=bill)
    return render(request, 'billing/billing_detail.html', {'bill_form': bill_form, 'coupon': coupon})


def bills(request):
    bills = Bill.objects.filter(status=1).order_by('-created')
    total_bills = bills.count()
    paginator = Paginator(bills, 12)
    page = request.GET.get('page')
    try:
        bills = paginator.page(page)
    except PageNotAnInteger:
        bills = paginator.page(1)
    except EmptyPage:
        bills = paginator.page(paginator.num_pages)
    return render(request, 'billing/bills.html', {'bills': bills, 'page': page, 'total_bills': total_bills})