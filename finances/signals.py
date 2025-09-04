from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from finances.models import Profile


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
