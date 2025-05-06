import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from finances.models import Transaction, Categorie, Account
from finances.forms import TransactionModelForm, CategorieModelForm, AccountModelForm
from app import metrics

# Create your views here.


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TransactionModelForm()
        context["form_categories"] = CategorieModelForm()
        context["form_accounts"] = AccountModelForm()
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
        transaction = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        return JsonResponse({
            "id": transaction.id,
            "description": transaction.description,
            "category_id": transaction.category.id,
            "category_name": transaction.category.category,
            "account_id": transaction.account.id,
            "account_name": transaction.account.name,
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
        transaction.value = data.get("value", transaction.value)

        transaction.save()

        return JsonResponse({"message": "Transacao atualizada com sucesso"})


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy()

    def delete(self, request, *args, **kwargs):
        transaction = get_object_or_404(
            Transaction, pk=self.kwargs['pk'], user=self.request.user)
        transaction.delete()

        return JsonResponse({"success": "True"})


class CategorieCreateView(CreateView):
    model = Categorie
    form_class = CategorieModelForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)  # Decodifica JSON
            form = self.form_class(data)

            if form.is_valid():
                form.save()
                return JsonResponse({"success": True})

            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)


class AccountCreateView(CreateView):
    model = Account
    form_class = AccountModelForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            form = self.form_class(data)

            if form.is_valid():
                form.save()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "errors": "JSON inválido"}, status=400)


class DashboardListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'dashboard.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = super().get_queryset()

    def sum_values(self):
        transactions = Transaction.objects.all()
        total_value = sum(transaction.value for transaction in transactions)
        return total_value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TransactionModelForm()
        context["form_categories"] = CategorieModelForm()
        context["form_accounts"] = AccountModelForm()
        context["transactions_metrics"] = metrics.get_transactions_value()
        return context
