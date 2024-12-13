from django.shortcuts import render
from django.urls import reverse_lazy
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


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionModelForm
    template_name = 'transaction_update.html'

    def get_success_url(self):
        return reverse_lazy('transaction-list')


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transaction_delete.html'
    success_url = '/transactions/'
