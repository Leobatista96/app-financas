from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from datetime import datetime
from finances.models import Profile, Transaction


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal para criar profile do usuário automaticamente.
    Se o profile já existir (criado pelo form), não sobrescreve.
    """
    if created:
        # Verifica se o profile já foi criado pelo formulário
        if not hasattr(instance, 'profile'):
            Profile.objects.get_or_create(user=instance)


# @receiver(post_save, sender=Transaction)
# def send_transactions_event(sender, instance, **kwargs):
#     notify = Notify()

#     data = {
#         "event_type": "create_transaction",
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "description": instance.description,
#         "value": instance.value,
#         "account": instance.account.name,
#         "category": instance.category.category,
#         "due_date": str(instance.due_date),
#     }

#     notify.send_event(data)