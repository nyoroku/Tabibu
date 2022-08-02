from django import forms

from .models import Transaction


class TransAddForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('client', 'item', 'quantity')





