from rest_framework import serializers

from accounts.models import Account
from categories.models import Categorie
from finances.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'value', 'description',
                  'due_date', 'account', 'category',]

    # user = serializers.StringRelatedField(read_only=True)
    # account = serializers.StringRelatedField(read_only=True)
    # category = serializers.StringRelatedField(read_only=True)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user', 'name', 'value',
                  'categorie',]

    user = serializers.StringRelatedField(read_only=True)
    categorie = serializers.StringRelatedField(read_only=True)


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['user', 'category', 'category_type', ]

    user = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
