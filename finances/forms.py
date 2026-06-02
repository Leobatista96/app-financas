from django import forms
from finances.models import Transaction, Categorie, Account


class TransactionModelForm(forms.ModelForm):

    due_date = forms.DateField(
        widget=forms.SelectDateWidget, 
        required=True,        
    )

    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ['user']
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)
            self.fields['category'].queryset = Categorie.objects.filter(user=user)



class CategorieModelForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Categorie.objects.filter(user=user)


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name'].queryset = Account.objects.filter(user=user)