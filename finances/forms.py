from django import forms

from finances.models import Account, Categorie, Transaction


class TransactionModelForm(forms.ModelForm):

    # DateInput nativo (type="date") para ficar igual ao modal de atualização,
    # que usa <input type="date" class="form-control">. Envia YYYY-MM-DD.
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
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
