import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError, Sum
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

    def get_queryset(self):
        accounts = Account.objects.filter(
            user=self.request.user).select_related('user')
        return accounts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_balance = Account.objects.filter(
            user=self.request.user).aggregate(total=Sum('value'))['total'] or 0
        context['transactions_metrics'] = get_transactions_value(
            user=self.request.user)
        context['form'] = TransactionModelForm(user=self.request.user)
        context['form_accounts'] = AccountModelForm(user=self.request.user)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['total_balance'] = total_balance
        return context


class AccountCreateView(CreateView):
    model = Account
    form_class = AccountModelForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            form = self.form_class(data)

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
