from django.db import models

class Accounts(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome da Conta')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome da Categoria')
    type = models.CharField(max_length=100, choices=[('Receita', 'Receita'), ('Despesa', 'Despesa')], verbose_name='Tipo de Categoria')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    value = models.FloatField(verbose_name='Valor')
    description = models.CharField(max_length=150, blank=True, default= '',verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    account = models.ForeignKey(Accounts, on_delete=models.PROTECT, related_name='transaction_accounts', verbose_name='Conta')
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='transaction_categories', verbose_name='Categoria')

    def __str__(self):
        return self.description


