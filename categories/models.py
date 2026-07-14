from django.contrib.auth.models import User
from django.db import models


class Categorie(models.Model):

    CATEGORY_TYPE_CHOICES = [
        ('revenue', 'Receita'),
        ('expense', 'Despesa'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_categorie', verbose_name='Usuário')
    category = models.CharField(
        max_length=100, unique=True, verbose_name='Categoria')
    category_type = models.CharField(
        max_length=10, choices=CATEGORY_TYPE_CHOICES, default='revenue', verbose_name='Tipo de Categoria')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Última Atualização')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ('user', 'category')

    def __str__(self):
        return self.category
