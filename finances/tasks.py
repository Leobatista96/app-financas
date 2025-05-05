import datetime
from celery import shared_task
from .models import Transaction, Profile
from app.services.evolution_api import EvolutionAPI


@shared_task
def teste_task():
    evolution_api = EvolutionAPI()
    transactions = Transaction.objects.all()
    profiles = Profile.objects.all()
    today_less_1 = datetime.timedelta(days=1)
    today = datetime.date.today()
    for transaction in transactions:

        description = transaction.description
        category = transaction.category.category
        account = transaction.account.name
        value = transaction.value
        user = transaction.user.username
        due_date = transaction.due_date
        if (due_date - today_less_1) == today:
            for profile in profiles:
                phone_number = profile.phone_number
            message = (f"""
                Descrição: {description}
                Categoria: {category}
                Conta: {account}
                Valor: {value}
                Data de Vencimento: {due_date}
                Usuário: {user}
                Telefone: {phone_number}
            """)
            evolution_api.send_whatsapp_message(
                message=message,
                number=phone_number
            )
