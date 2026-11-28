import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, FloatField, ProtectedError, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.forms import AccountModelForm
from accounts.models import Account
from app.metrics import get_transactions_value
from finances.forms import TransactionModelForm


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts.html'
    # Nome usado pelo template ({% for account in accounts %}); expõe a queryset
    # ANOTADA com o saldo real — não sobrescrever no get_context_data.
    context_object_name = 'accounts'

    def get_queryset(self):
        # Saldo real por conta: receitas − despesas das transações da conta,
        # em uma única query (agregados filtrados). Contas sem movimentação = 0.
        return (
            Account.objects.filter(user=self.request.user)
            .select_related('user')
            .annotate(
                entradas=Coalesce(
                    Sum('transaction_accounts__value',
                        filter=Q(transaction_accounts__category__category_type='revenue')),
                    Value(0.0), output_field=FloatField()),
                saidas=Coalesce(
                    Sum('transaction_accounts__value',
                        filter=Q(transaction_accounts__category__category_type='expense')),
                    Value(0.0), output_field=FloatField()),
            )
            .annotate(saldo=F('entradas') - F('saidas'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions_metrics'] = get_transactions_value(
            user=self.request.user)
        context['form'] = TransactionModelForm(user=self.request.user)
        context['form_accounts'] = AccountModelForm(user=self.request.user)
        return context


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountModelForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            form = self.form_class(data, user=request.user)

            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'errors': 'JSON inválido'}, status=400)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account

    def get_object(self, queryset=...):
        return get_object_or_404(Account, pk=self.kwargs['pk'], user=self.request.user)

    def get(self, request, *args, **kwargs):
        accounts = self.get_object()
        return JsonResponse({
            "name": accounts.name,
            "value": accounts.value,
            "categorie": accounts.categorie,
        })

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = reverse_lazy("account-list")

    def delete(self, request, *args, **kwargs):
        objects = ProtectedError.protected_objects
        if objects:
            context = self.get_context_data(
                error_message='Erro',
            )
            return self.render_to_response(context)
        account = get_object_or_404(
            Account, pk=self.kwargs['pk'], user=self.request.user,
        )
        account.delete()
        return account
