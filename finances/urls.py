from django.urls import path
from django.contrib.auth import views as auth_views
from finances.views import TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView, CategorieCreateView, AccountCreateView


urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('new_transaction/', TransactionCreateView.as_view(),
         name='transaction-create'),
    path('transactions/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction-delete'),

    path('new_categorie/', CategorieCreateView.as_view(), name='categorie-create'),

    path('new_account/', AccountCreateView.as_view(), name='account-create'),
]
