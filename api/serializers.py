from rest_framework.serializers import ModelSerializer
from finances.models import Transaction, Account, Categorie

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class CategorieSerializer(ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

