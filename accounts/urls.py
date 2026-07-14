from django.urls import path

from accounts.views import AccountCreateView, AccountListView

urlpatterns = [
    path('new_account/', AccountCreateView.as_view(), name='account-create'),
    path('account/', AccountListView.as_view(), name='account-list'),
]
