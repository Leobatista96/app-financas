import datetime
from celery import shared_task
from .models import Transaction, Profile
from app.services.evolution_api import EvolutionAPI


@shared_task
def teste_task():
    try:
        evolution_api = EvolutionAPI()
        transactions = Transaction.objects.all()
        profiles = Profile.objects.all()
        
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        
        transactions_due_tomorrow = transactions.filter(due_date=tomorrow)
        
        if not transactions_due_tomorrow.exists():
            return "Nenhuma transação vence amanhã"
        
        if not profiles.exists():
            return "Nenhum perfil encontrado para enviar mensagens"
        
        messages_sent = 0
        
        for transaction in transactions_due_tomorrow:
            description = transaction.description
            category = transaction.category.category if transaction.category else "Sem categoria"
            account = transaction.account.name if transaction.account else "Sem conta"
            value = transaction.value
            user = transaction.user.username if transaction.user else "Sem usuário"
            due_date = transaction.due_date
            
            message = f"""
🔔 LEMBRETE DE VENCIMENTO
                
Descrição: {description}
Categoria: {category}
Conta: {account}
Valor: R$ {value}
Data de Vencimento: {due_date.strftime('%d/%m/%Y')}
Usuário: {user}
            """
            
            # Enviar para todos os perfis
            for profile in profiles:
                phone_number = profile.phone_number
                if phone_number:
                    try:
                        evolution_api.send_whatsapp_message(
                            message=message,
                            number=phone_number
                        )
                        messages_sent += 1
                    except Exception as e:
                        print(f"Erro ao enviar mensagem para {phone_number}: {e}")
        
        return f"Task executada com sucesso. {messages_sent} mensagens enviadas."
        
    except Exception as e:
        return f"Erro na execução da task: {str(e)}"
