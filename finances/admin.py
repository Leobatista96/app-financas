from django.contrib import admin

from finances.models import Profile, Transaction


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number',]
    search_fields = ['user', 'phone_number',]
    exclude = ['user',]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'value',
                    'category', 'due_date', 'created_at', 'updated_at', 'user',]
    search_fields = ['category', 'value',
                     'description', 'due_date', 'created_at', 'updated_at', 'user',]

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Profile, ProfileAdmin)
