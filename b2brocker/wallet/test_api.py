from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from wallet.models import Transaction, Wallet
from wallet.factory import ext_decimal, wallet_factory, transaction_factory, pseudo_random, mf


class TransactionAPITestCase(APITestCase):
    """
    Test Transaction API
    """

    def setUp(self):
        self.wallet = wallet_factory(obj_num=1)[0]
        self.wallet.save()
        self.transaction_url = reverse('transaction-list')

    def test_create_transaction(self):
        """Create transaction"""
        amount = ext_decimal(start=0.0, end=1000.0)
        transaction = transaction_factory(wallet=self.wallet, obj_num=1,
                                          amount=amount)[0]
        data = {
            'wallet': self.wallet.id,
            'txid': transaction.txid,
            'amount': transaction.amount,
        }
        response = self.client.post(self.transaction_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().amount, amount)

    def test_list_transactions(self):
        """List transaction with paginator"""
        obj_num = pseudo_random.randint(30, 40)
        transactions = transaction_factory(wallet=self.wallet, obj_num=obj_num)
        Transaction.objects.bulk_create(transactions)

        response1 = self.client.get(self.transaction_url)
        response2 = self.client.get(self.transaction_url + '?page=2')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['count'], obj_num)
        self.assertEqual(len(response1.data['results']), 10)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['count'], obj_num)
        self.assertEqual(len(response2.data['results']), 10)

    def test_negative_balance(self):
        """Transaction for negative balance can not be save"""
        amount1 = ext_decimal(start=1.0, end=5.0)
        amount2 = ext_decimal(start=-20.0, end=-10.0)
        transaction1 = transaction_factory(wallet=self.wallet, obj_num=1,
                                           amount=amount1, id=None)[0]
        transaction2 = transaction_factory(wallet=self.wallet, obj_num=1,
                                           amount=amount2, id=None)[0]
        data1 = {
            'wallet': self.wallet.id,
            'txid': transaction1.txid,
            'amount': transaction1.amount,
        }
        data2 = {
            'wallet': self.wallet.id,
            'txid': transaction2.txid,
            'amount': transaction2.amount,
        }

        response1 = self.client.post(self.transaction_url, data1,
                                     format='json')
        response2 = self.client.post(self.transaction_url, data2,
                                     format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_wallet(self):
        """Filter amount by wallet"""
        wallet1, wallet2 = wallet_factory(obj_num=2)
        Wallet.objects.bulk_create([wallet1, wallet2, ])
        t1 = transaction_factory(wallet=wallet1, obj_num=3, id=None)
        t2 = transaction_factory(wallet=wallet2, obj_num=3, id=None)
        Transaction.objects.bulk_create(t1 + t2)
        data = {
            'wallet': wallet1.id,
        }

        response1 = self.client.get(self.transaction_url)
        response2 = self.client.get(self.transaction_url, data)

        self.assertEqual(len(response1.data['results']), 6)
        self.assertEqual(len(response2.data['results']), 3)
        for t in response2.data['results']:
            self.assertEqual(t['wallet'], wallet1.id)

    def test_filter_txid(self):
        transactions = transaction_factory(wallet=self.wallet, obj_num=10,
                                           id=None)
        Transaction.objects.bulk_create(transactions)
        data = {
            'txid': transactions[0].txid,
        }

        response = self.client.get(self.transaction_url, data)

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['txid'],
                         transactions[0].txid)

    def test_required_fields(self):
        """Required fields must be set in data"""
        rf = [
            'wallet',
            'txid',
            'amount',
        ]
        amount = ext_decimal(start=0.0, end=1000.0)
        transaction = transaction_factory(wallet=self.wallet, obj_num=1,
                                          amount=amount)[0]
        core_data = {
            'wallet': self.wallet.id,
            'txid': transaction.txid,
            'amount': transaction.amount,
        }
        for f in rf:
            data = {
                **core_data
            }
            del data[f]
            response = self.client.post(self.transaction_url, data,
                                        format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WalletAPITestCase(APITestCase):
    """
    Test Wallet API
    """

    def setUp(self):
        self.wallet_url = reverse('wallet-list')

    def test_create_wallet(self):
        """Test create wallet"""
        wallet = wallet_factory(obj_num=1)[0]
        data = {
            'label': wallet.label,
        }

        response = self.client.post(self.wallet_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertEqual(Wallet.objects.get().label, wallet.label)

    def test_list(self):
        """List wallets with paginator"""
        obj_num = pseudo_random.randint(30, 40)
        transactions = wallet_factory(obj_num=obj_num)
        Wallet.objects.bulk_create(transactions)

        response1 = self.client.get(self.wallet_url)
        response2 = self.client.get(self.wallet_url + '?page=2')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['count'], obj_num)
        self.assertEqual(len(response1.data['results']), 10)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['count'], obj_num)
        self.assertEqual(len(response2.data['results']), 10)

    def test_filter_by_label(self):
        """Test filter wallets by label"""
        label = mf('name')
        wallets = wallet_factory(obj_num=2)
        wallets[0].label = label
        Wallet.objects.bulk_create(wallets)
        data = {
            'label': label,
        }

        response = self.client.get(self.wallet_url, data)

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['label'], label)

    def test_required_field(self):
        """Test post wallet data without label"""
        data = {}

        response = self.client.post(self.wallet_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
