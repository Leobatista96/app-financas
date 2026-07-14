from django.urls import path

from finances.views import (DashboardListView, TransactionCreateView,
                            TransactionDeleteView, TransactionListView,
                            TransactionUpdateView)

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('new_transaction/', TransactionCreateView.as_view(),
         name='transaction-create'),
    path('transactions/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction-delete'),




    path('dashboard/', DashboardListView.as_view(), name='dashboard-list'),
]
