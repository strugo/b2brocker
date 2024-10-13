from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['label', 'balance']
    filterset_fields = ['label']


class TransactionViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['txid', 'amount', 'wallet']
    filterset_fields = ['wallet', 'txid']
