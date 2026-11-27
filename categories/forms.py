from django import forms

from categories.models import Categorie


class CategorieModelForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_category(self):
        # unique_together('user', 'category') não é validada pelo ModelForm
        # porque 'user' está em exclude — validamos aqui, por usuário.
        category = self.cleaned_data.get('category')
        if category and self.user and Categorie.objects.filter(
                user=self.user, category=category).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                'Você já tem uma categoria com este nome.')
        return category
