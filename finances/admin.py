from django.contrib import admin
from finances.models import Account, Transaction, Categorie


class AccountsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at',]
    search_fields = ['name', 'created_at', 'updated_at', ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'value',
                    'category', 'created_at', 'updated_at',]
    search_fields = ['category', 'value',
                     'description', 'created_at', 'updated_at',]


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['category', 'created_at', 'updated_at',]
    search_fields = ['category', 'created_at', 'updated_at',]


admin.site.register(Account, AccountsAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Categorie, CategoriesAdmin)
