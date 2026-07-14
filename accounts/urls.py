from django.urls import path

from accounts.views import (AccountCreateView, AccountDeleteView,
                            AccountListView, AccountUpdateView)

urlpatterns = [
    path('new_account/', AccountCreateView.as_view(), name='account-create'),
    path('account/', AccountListView.as_view(), name='account-list'),
    path('account/<int:pk>/update',
         AccountUpdateView.as_view(), name='account-update'),
    path('account/<int:pk>/delete',
         AccountDeleteView.as_view(), name='account-delete'),
]
