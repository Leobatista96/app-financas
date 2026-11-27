from django import forms

from finances.models import Account


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        # unique_together('user', 'name') não é validada pelo ModelForm
        # porque 'user' está em exclude — validamos aqui, por usuário.
        name = self.cleaned_data.get('name')
        if name and self.user and Account.objects.filter(
                user=self.user, name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Você já tem uma conta com este nome.')
        return name
