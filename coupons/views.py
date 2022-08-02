from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from billing.models import Bill
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            bill.coupon = bill
            coupon.save()
        except Coupon.DoesNotExist:
            return redirect('#')
    return redirect(request, bill.get_absolute_url())


