from django.db.models import Sum, Count
from finances.models import Transaction


def get_transactions_value():
    total_transactions_value = Transaction.objects.all(
    ).aggregate(Sum("value"))['value__sum']

    check_category_is_none = Transaction.objects.aggregate(
        Count('category'))['category__count']

    total_categories_revenues = Transaction.objects.filter(
        category__category__icontains='Receita').aggregate(Sum('value'))['value__sum']

    total_categories_expense = Transaction.objects.filter(
        category__category__icontains='Despesa').aggregate(Sum('value'))['value__sum']

    if total_categories_expense is None:
        return dict(
            total_categories_expense=0,
            total_transactions_value=total_transactions_value,
            total_categories_revenues=total_categories_revenues,
            balance=0,
        )

    if total_categories_revenues is None:
        return dict(
            total_categories_revenues=0,
            total_transactions_value=total_transactions_value,
            total_categories_expense=total_categories_expense,
            balance=0,
        )

    balance = total_categories_revenues - total_categories_expense

    return dict(
        total_transactions_value=total_transactions_value,
        total_categories_revenues=total_categories_revenues,
        total_categories_expense=total_categories_expense,
        balance=balance,
    )
