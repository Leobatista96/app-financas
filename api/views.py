from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAccountOwner, IsCategoryOwner, IsTransactionOwner
from finances.models import Account, Categorie, Transaction

from .serializers import (AccountSerializer, CategorieSerializer,
                          TransactionSerializer)


class Pagination(PageNumberPagination):
    page_size = 10


class TransactionCreateListAPIView(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, IsTransactionOwner,)
    pagination_class = Pagination


class TransactionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, IsTransactionOwner,)


class AccountCreateListAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated, IsAccountOwner,)


class AccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated, IsAccountOwner,)


class CategorieCreateListAPIView(ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = (IsAuthenticated, IsCategoryOwner,)


class CategorieRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = (IsAuthenticated, IsCategoryOwner,)
