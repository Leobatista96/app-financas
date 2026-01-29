from django.urls import path
from django.contrib.auth import views as auth_views
from finances.views import (
    TransactionListView, 
    TransactionCreateView, 
    TransactionUpdateView, 
    TransactionDeleteView, 
    CategorieCreateView,
    CategorieListView,
    AccountCreateView,
    AccountListView, 
    DashboardListView,
    RecipesListView,
    RevenuesListView,
)


urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('new_transaction/', TransactionCreateView.as_view(),
         name='transaction-create'),
    path('transactions/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction-delete'),

    path('new_categorie/', CategorieCreateView.as_view(), name='categorie-create'),
    path('categories/', CategorieListView.as_view(), name='categorie-list'),

    path('recipes/', RecipesListView.as_view(), name='recipes-list'),
    
    path('revenues/', RevenuesListView.as_view(), name='revenues-list'),

    path('new_account/', AccountCreateView.as_view(), name='account-create'),
    path('accounts/', AccountListView.as_view(), name='account-list'),

    path('dashboard/', DashboardListView.as_view(), name='dashboard-list'),
]
