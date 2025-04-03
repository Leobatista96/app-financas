from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome da Conta')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Última Atualização')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Categorie(models.Model):
    category = models.CharField(max_length=100, verbose_name='Categoria')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Última Atualização')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.category


class Transaction(models.Model):
    value = models.FloatField(verbose_name='Valor')
    description = models.CharField(
        max_length=150, blank=True, default='', verbose_name='Descrição')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Última Atualização')
    account = models.ForeignKey(Account, on_delete=models.PROTECT,
                                related_name='transaction_accounts', verbose_name='Conta')
    category = models.ForeignKey(Categorie, on_delete=models.PROTECT,
                                 related_name='transaction_categories', verbose_name='Categoria')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.description
