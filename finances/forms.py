from django import forms
from finances.models import Transaction, Categorie, Account, Recipes, Revenues


class TransactionModelForm(forms.ModelForm):

    due_date = forms.DateField(
        widget=forms.SelectDateWidget, 
        required=True,        
    )

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

    
class RecipesModelForm(forms.ModelForm):

    due_date = forms.DateField(
        widget=forms.SelectDateWidget,
        required=True,
    )

    class Meta:
        model = Recipes
        fields = '__all__'
        exclude = ['user']

class RevenuesModelForm(forms.ModelForm):

    due_date = forms.DateField(
        widget=forms.SelectDateWidget,
        required=True,
    )

    class Meta:
        model = Revenues
        fields = '__all__'
        exclude = ['user']