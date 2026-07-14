from django.contrib import admin

from categories.models import Categorie


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['category', 'category_type',
                    'created_at', 'updated_at', 'user',]
    search_fields = ['category', 'category_type',
                     'created_at', 'updated_at', 'user',]
    list_filter = ['category_type']

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Categorie, CategoriesAdmin)
