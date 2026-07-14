from django import forms

from finances.models import Account


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name'].queryset = Account.objects.filter(user=user)
