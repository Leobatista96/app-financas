from django.contrib.auth.models import User
from django.db import models

from accounts.models import Account
from categories.models import Categorie


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name='profile')
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Telefone',
        help_text='Número de telefone (ex: 11999999999)',
        default=''
    )
    created_at = models.DateTimeField(
        auto_now=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Última Atualização')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Perfil'

    def __str__(self):
        return f"Perfil de: {self.user.username}"


class Transaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user', verbose_name='Usuário')
    value = models.FloatField(verbose_name='Valor')
    description = models.CharField(
        max_length=150, blank=True, default='', verbose_name='Descrição')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Última Atualização')
    due_date = models.DateField(
        verbose_name='Data de Vencimento')
    account = models.ForeignKey(Account, on_delete=models.PROTECT,
                                related_name='transaction_accounts', verbose_name='Conta')
    category = models.ForeignKey(Categorie, on_delete=models.PROTECT,
                                 related_name='transaction_categories', verbose_name='Categoria')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    def __str__(self):
        return self.description
