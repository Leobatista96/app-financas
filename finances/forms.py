from django import forms

from finances.models import Account, Categorie, Transaction


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
            self.fields['category'].queryset = Categorie.objects.filter(
                user=user)
