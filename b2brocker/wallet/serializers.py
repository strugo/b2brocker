from rest_framework import serializers

from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance', 'created']
        read_only_fields = ['balance', 'created']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'txid', 'amount', 'created']
        read_only_fields = ['created', ]
