from celery import shared_task
from .models import Transaction, Profile
from app.services.evolution_api import EvolutionAPI


@shared_task
def teste_task():
    evolution_api = EvolutionAPI()
    transactions = Transaction.objects.all()
    profiles = Profile.objects.all()

    for transaction in transactions:
        description = transaction.description
        categoria = transaction.category.category
        conta = transaction.account.name
        valor = transaction.value
        user = transaction.user.username
        for profile in profiles:
            phone_number = profile.phone_number
        message = (f"""
            Descrição: {description}
            Categoria: {categoria}
            Conta: {conta}
            Valor: {valor}
            Usuário: {user}
            Telefone: {phone_number}
        """)
        evolution_api.send_whatsapp_message(
            message=message,
            number=phone_number
        )
