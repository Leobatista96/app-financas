from django.db.models import Sum, Count
from finances.models import Transaction


def get_transactions_value(user):
    total_transactions_values = Transaction.objects.filter(
        user=user).aggregate(Sum("value"))['value__sum']

    total_categories_revenues = Transaction.objects.filter(
        category__category__icontains='Receita', user=user).aggregate(Sum('value'))['value__sum']

    total_categories_expenses = Transaction.objects.filter(
        category__category__icontains='Despesa', user=user).aggregate(Sum('value'))['value__sum']

    if total_categories_revenues is None:
        total_categories_revenues = 0

    if total_categories_expenses is None:
        total_categories_expenses = 0

    balance = total_categories_revenues - total_categories_expenses

    return dict(
        total_transactions_value=total_transactions_values,
        total_categories_revenue=total_categories_revenues,
        total_categories_expense=total_categories_expenses,
        balance=balance,
    )
