from django.contrib import admin
from finances.models import Account, Transaction, Categorie, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number',]
    search_fields = ['user', 'phone_number',]
    exclude = ['user',]


class AccountsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at',]
    search_fields = ['name', 'created_at', 'updated_at', ]
    exclude = ['user',]

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'value',
                    'category', 'due_date', 'created_at', 'updated_at', 'user',]
    search_fields = ['category', 'value',
                     'description', 'due_date', 'created_at', 'updated_at', 'user',]
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['category', 'created_at', 'updated_at',]
    search_fields = ['category', 'created_at', 'updated_at',]
    exclude = ['user',]

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Account, AccountsAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Categorie, CategoriesAdmin)
admin.site.register(Profile, ProfileAdmin)
