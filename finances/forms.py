from django import forms
from finances.models import Transaction


class TransactionModelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
