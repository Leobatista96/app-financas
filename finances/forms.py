from django import forms
from finances.models import Transaction, Categorie, Account, Profile


class TransactionModelForm(forms.ModelForm):

    due_date = forms.DateField(
        widget=forms.SelectDateWidget, required=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ['user']


class CategorieModelForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'
        exclude = ['user']


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user']
