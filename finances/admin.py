from django.contrib import admin
from finances.models import Account, Transaction, Categorie


class AccountsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'created_at']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'value', 'created_at', 'category',]
    search_fields = ['category', 'description', 'created_at',]


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['category',]
    search_fields = ['category']


admin.site.register(Account, AccountsAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Categorie, CategoriesAdmin)
