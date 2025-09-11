from django.urls import path
from .views import TransactionCreateListAPIView, TransactionRetrieveUpdateDestroyAPIView, AccountCreateListAPIView, AccountRetrieveUpdateDestroyAPIView, CategorieCreateListAPIView, CategorieRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('transactions/', TransactionCreateListAPIView.as_view(), name='api-transactions-list'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyAPIView.as_view(), name='api-transactions-retrieve-update-destroy'),

    path('categories/', CategorieCreateListAPIView.as_view(), name='api-categories-list'),
    path('categories/<int:pk>/', CategorieRetrieveUpdateDestroyAPIView.as_view(), name='api-categories-retrieve-update-destroy'),

    path('accounts/', AccountCreateListAPIView.as_view(), name='api-accounts-list'),
    path('accounts/<int:pk>/', AccountRetrieveUpdateDestroyAPIView.as_view(), name='api-account-retrieve-update-destroy'),
]