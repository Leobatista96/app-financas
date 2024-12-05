from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from finances.models import Transaction
from finances.forms import TransactionModelForm

# Create your views here.


def dashboard_view(request):
    return render(request, 'dashboard.html')


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        transactions = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            transactions = transactions.filter(
                category__category__icontains=search)
            return transactions
        return Transaction.objects.all()


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionModelForm
    template_name = 'new_transaction.html'
    success_url = '/transactions/'
