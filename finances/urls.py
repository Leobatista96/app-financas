from django.contrib import admin
from django.urls import path
from finances.views import dashboard_view, TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView


urlpatterns = [
    path('/', dashboard_view, name='dashboard-url'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('new_transaction/', TransactionCreateView.as_view(),
         name='transaction-create'),
    path('transactions/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction-delete'),
]
