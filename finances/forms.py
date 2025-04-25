from django import forms
from finances.models import Transaction, Categorie, Account


class TransactionModelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ['user']


class CategorieModelForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
