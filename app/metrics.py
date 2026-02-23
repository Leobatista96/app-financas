from django.db.models import Sum, Count
from finances.models import Transaction


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


def get_graphics_data(user):

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

    categories_labels = [item['category__category'] for item in categories_data]
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