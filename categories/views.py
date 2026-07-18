import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import CreateView, ListView

from app.metrics import get_transactions_value
from categories.forms import CategorieModelForm
from categories.models import Categorie


class CategorieListView(LoginRequiredMixin, ListView):
    model = Categorie
    template_name = 'categories.html'

    def get_queryset(self):
        categories = Categorie.objects.filter(
            user=self.request.user).select_related('user')
        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions_metrics"] = get_transactions_value(
            user=self.request.user)
        context["form_categories"] = CategorieModelForm(user=self.request.user)
        context["categories"] = Categorie.objects.filter(
            user=self.request.user)

        categories_revenues_filter = Categorie.objects.filter(
            user=self.request.user, category_type='revenue')
        context["categories_revenues_filter"] = categories_revenues_filter
        return context


class CategorieCreateView(CreateView):
    model = Categorie
    form_class = CategorieModelForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)  # Decodifica JSON
            form = self.form_class(data)
            if form.is_valid():
                categorie = form.save(commit=False)
                categorie.user = request.user
                categorie.save()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
