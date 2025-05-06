from django.db.models import Sum
from finances.models import Transaction


def get_transactions_value():
    transactions = Transaction.objects.all()
    total_transactions_value = sum(
        transaction.value for transaction in transactions)

    return dict(
        total_transactions_value=total_transactions_value,
    )
