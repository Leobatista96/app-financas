from django import forms

from categories.models import Categorie


class CategorieModelForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Categorie.objects.filter(
                user=user)
