
from django.db.models import Sum
from django.db.models.functions import ExtractMonth

from accounts.models import Account
from finances.models import Transaction

MONTHS = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro',
}


def get_transactions_value(user):
    total_transactions_values = Transaction.objects.filter(
        user=user).aggregate(Sum("value"))['value__sum']

    total_categories_revenues = Transaction.objects.filter(
        category__category_type='revenue', user=user).aggregate(Sum('value'))['value__sum']

    total_categories_expenses = Transaction.objects.filter(
        category__category_type='expense', user=user).aggregate(Sum('value'))['value__sum']

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


def get_category_graphics_data(user):

    total_recipes = Transaction.objects.filter(
        user=user,
        category__category_type='revenue',
    ).count()

    total_expenses = Transaction.objects.filter(
        user=user,
        category__category_type='expense',
    ).count()

    categories_data = Transaction.objects.filter(
        user=user,
    ).values('category__category').annotate(total=Sum('value')).order_by('-total')

    categories_labels = [item['category__category']
                         for item in categories_data]
    categories_values = [float(item['total']) for item in categories_data]

    return {
        'total_recipes': {
            'labels': ['Receitas', 'Despesas'],
            'data': [total_recipes, total_expenses],
        },
        'categories': {
            'labels': categories_labels,
            'values': categories_values,
        }
    }


def get_montly_graphics_metric(user):
    total_value_by_month_expense = Transaction.objects.filter(user=user, category__category_type='expense').annotate(
        month=ExtractMonth('due_date')).values('month').annotate(total=Sum('value')).order_by('month')
    total_value_by_month_revenue = Transaction.objects.filter(user=user, category__category_type='revenue').annotate(
        month=ExtractMonth('due_date')).values('month').annotate(total=Sum('value')).order_by('month')

    month_labels = [MONTHS[item['month']]
                    for item in total_value_by_month_expense]
    total_month_value_expense = [item['total']
                                 for item in total_value_by_month_expense]
    total_month_value_revenue = [item['total']
                                 for item in total_value_by_month_revenue]

    return {
        'month_labels': month_labels,
        'total_month_value_expense': total_month_value_expense,
        'total_month_value_revenue': total_month_value_revenue,
    }
