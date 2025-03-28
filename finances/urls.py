from django.contrib import admin
from django.urls import path
from finances.views import TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView


urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('new_transaction/', TransactionCreateView.as_view(),
         name='transaction-create'),
    path('transactions/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction-delete'),
]
