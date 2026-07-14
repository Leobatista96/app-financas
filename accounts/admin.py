from django.contrib import admin

from accounts.models import Account


class AccountsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'categorie',
                    'created_at', 'updated_at', 'user',]
    search_fields = ['name', 'value', 'categorie',
                     'created_at', 'updated_at', 'user',]

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Account, AccountsAdmin)
