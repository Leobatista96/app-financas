from django.urls import path

from categories.views import CategorieCreateView, CategorieListView

urlpatterns = [
    path('new_categorie/', CategorieCreateView.as_view(), name='categorie-create'),
    path('categories/', CategorieListView.as_view(), name='categorie-list'),
]
