from django.core.management.base import BaseCommand
from app.services.evolution_api import EvolutionAPI
from finances.models import Transaction


class Command(BaseCommand):

    def handle(self, *args, **options):
        evolution_api = EvolutionAPI()
        transactions = Transaction.objects.all()
        print(f"Total de Transacoes: {transactions.count()}")

        for transaction in transactions:

            descricao = transaction.description
            conta = transaction.account.name
            categoria = transaction.category.category
            valor = transaction.value
            criado_em = transaction.created_at.strftime("%d/%m/%Y")

            mensagem = f" Descricão: {descricao}\n Conta: {conta}\n Categoria: {categoria}\n Valor: {valor}\n Criado em: {criado_em}"
            evolution_api.send_whatsapp_message(mensagem)
