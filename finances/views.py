import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.forms import AccountModelForm
from accounts.models import Account
from app.metrics import (get_category_graphics_data,
                         get_montly_graphics_metric, get_transactions_value)
from categories.forms import CategorieModelForm
from categories.models import Categorie
from finances.forms import TransactionModelForm
from finances.models import Transaction

# Create your views here.


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction.html'
    context_object_name = 'transactions'
    paginate_by = 5

    def get_queryset(self):
        transaction = Transaction.objects.filter(
            user=self.request.user).select_related('account', 'category')
        return transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TransactionModelForm(user=self.request.user)
        context["form_categories"] = CategorieModelForm(user=self.request.user)
        context["form_accounts"] = AccountModelForm(user=self.request.user)
        context["transactions_metrics"] = get_transactions_value(
            user=self.request.user)
        context["categories"] = Categorie.objects.filter(
            user=self.request.user)
        context["accounts"] = Account.objects.filter(user=self.request.user)
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionModelForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)  # Decodifica JSON
            form = self.form_class(data)

            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({"success": True})

            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionModelForm

    def get_success_url(self):
        return reverse_lazy('transaction-list')

    def get_object(self):
        return get_object_or_404(Transaction, pk=self.kwargs['pk'], user=self.request.user)

    def get(self, request, *args, **kwargs):
        transaction = self.get_object()
        return JsonResponse({
            "id": transaction.id,
            "description": transaction.description,
            "category_id": transaction.category.id,
            "category_name": transaction.category.category,
            "account_id": transaction.account.id,
            "account_name": transaction.account.name,
            "due_date": transaction.due_date,
            "value": transaction.value,
            "created_at": transaction.created_at.strftime('%Y-%m-%d'),
        })

    def post(self, request, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        data = json.loads(request.body)

        transaction.description = data.get(
            "description", transaction.description)
        transaction.category_id = data.get("category", transaction.category.id)
        transaction.account_id = data.get("account", transaction.account.id)
        transaction.due_date = data.get("due_date", transaction.due_date)
        transaction.value = data.get("value", transaction.value)

        transaction.save()

        return JsonResponse({"message": "Transação atualizada com sucesso"})


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy()

    def delete(self, request, *args, **kwargs):
        transaction = get_object_or_404(
            Transaction, pk=self.kwargs['pk'], user=self.request.user)
        transaction.delete()

        return JsonResponse({"success": "True"})


class DashboardListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'dashboard.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TransactionModelForm(user=self.request.user)
        context["form_categories"] = CategorieModelForm(user=self.request.user)
        context["form_accounts"] = AccountModelForm(user=self.request.user)
        context["transactions_metrics"] = get_transactions_value(
            user=self.request.user)
        category_metrics = get_category_graphics_data(user=self.request.user)
        context['category_graphics_metrics'] = json.dumps(category_metrics)
        montly_metrics = get_montly_graphics_metric(user=self.request.user)
        context['montly_graphics_metrics'] = json.dumps(montly_metrics)
        return context
