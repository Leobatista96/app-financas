from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    CATEGORIE_CHOICES = [
        ('conta corrente', 'Conta Corrente'),
        ('dinheiro', 'Dinheiro'),
        ('poupanca', 'Poupança'),
        ('investimentos', 'Investimentos'),
        ('vale', 'VR/VA'),
        ('outros', 'Outros'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_account', verbose_name='Usuário')
    name = models.CharField(max_length=100, unique=True,
                            verbose_name='Nome da Conta')
    value = models.FloatField(verbose_name='Valor', default=0)
    categorie = models.CharField(max_length=100, choices=CATEGORIE_CHOICES,
                                 verbose_name='Categoria da Conta', default='Conta Corrente')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Última Atualização')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    def __str__(self):
        return self.name
