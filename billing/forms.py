from .models import Bill, BillItem
from django import forms
from django.forms import inlineformset_factory
from coupons.models import Coupon
from django.utils import timezone

class BillAddForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('status',)


class BillIForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('status', )


class CouponApplyForm(forms.ModelForm):

    class Meta:
        model = Bill
        fields = ('coupon', )

    def __init__(self, *args, **kwargs):

        super(CouponApplyForm, self).__init__()
        self.fields['coupon'] = forms.ModelChoiceField(queryset=Coupon.objects.all(), widget=forms.TextInput)

    def clean(self):
        code = Coupon.code
        now = timezone.now()
        try:
            Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
        except Coupon.DoesNotExist:
            Coupon.code = None



InvoiceFormSet = inlineformset_factory(Bill, BillItem, fields=['item', 'quantity'], extra=2, can_delete=True)