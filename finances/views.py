import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from finances.models import Transaction
from finances.forms import TransactionModelForm

# Create your views here.


def dashboard_view(request):
    return render(request, 'dashboard.html')


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction.html'
    context_object_name = 'transactions'
    paginate_by = 10

    # def get_queryset(self):
    #     transactions = super().get_queryset()
    #     search = self.request.GET.get('search')
    #     if search:
    #         transactions = transactions.filter(
    #             category__category__icontains=search)
    #         return transactions
    #     return Transaction.objects.all()
    def get_queryset(self):
        return Transaction.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_value'] = Transaction.objects.aggregate(
            total_value=Sum('value')
        )['total_value'] or 0
        return context


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionModelForm
    template_name = 'new_transaction.html'
    success_url = '/transactions/'


@method_decorator(csrf_exempt, name='dispatch')
class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionModelForm
    template_name = 'transaction_update.html'

    def get_success_url(self):
        return reverse_lazy('transaction-list')

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
        transaction.created_at = data.get("created_at", transaction.created_at)

        transaction.save()

        return JsonResponse({"message": "Transacao atualizada com sucesso"})


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transaction_delete.html'
    success_url = '/transactions/'
