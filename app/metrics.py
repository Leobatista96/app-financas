from django.db.models import Sum
from finances.models import Transaction


def get_transactions_value():
    total_transactions_value = Transaction.objects.all(
    ).aggregate(Sum("value"))['value__sum']

    total_categories_revenues = Transaction.objects.filter(
        category__category__icontains='Receita').aggregate(Sum('value'))['value__sum']

    total_categories_expense = Transaction.objects.filter(
        category__category__icontains='Despesa').aggregate(Sum('value'))['value__sum']

    balance = total_categories_revenues - total_categories_expense

    return dict(
        total_transactions_value=total_transactions_value,
        total_categories_revenue=total_categories_revenues,
        total_categories_expense=total_categories_expense,
        balance=balance,
    )
