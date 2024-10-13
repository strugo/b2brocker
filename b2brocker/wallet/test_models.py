from django.core.exceptions import ValidationError
from django.test import TestCase

from wallet.factory import ext_decimal, wallet_factory, transaction_factory


class WalletTestCase(TestCase):
    """
    Test for Wallet model
    """

    def test_positive_balance(self):
        """Positive balance is save"""
        balance = ext_decimal(start=0.0, end=1000.0)
        wallet = wallet_factory(obj_num=1, balance=balance)[0]

        wallet.save()

        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, balance)

    def test_negative_blance(self):
        """Negative balance do not save"""
        balance = ext_decimal(start=-1000.0, end=-1.0)
        wallet = wallet_factory(obj_num=1, balance=balance)[0]

        with self.assertRaises(ValueError):
            wallet.save()


class TransactionTestCase(TestCase):
    """
    Test for Transaction model
    """

    def setUp(self):
        wallet = wallet_factory(obj_num=1, balance=0)[0]
        wallet.save()
        self.wallet = wallet

    def test_count_balance(self):
        """Test count balance"""
        amount1 = ext_decimal(start=10.0, end=20.0)
        amount2 = ext_decimal(start=-5.0, end=-3.0)
        balance = amount1 + amount2
        transaction1 = transaction_factory(wallet=self.wallet, obj_num=1,
                                           amount=amount1, id=None)[0]
        transaction2 = transaction_factory(wallet=self.wallet, obj_num=1,
                                           amount=amount2, id=None)[0]

        transaction1.save()
        transaction2.save()
        self.wallet.refresh_from_db()

        self.assertEqual(balance, self.wallet.balance)

    def test_negative_balance(self):
        """Negative balance do not save"""
        amount1 = ext_decimal(start=1.0, end=5.0)
        amount2 = ext_decimal(start=-20.0, end=-10.0)
        transaction1 = transaction_factory(wallet=self.wallet, obj_num=1,
                                           amount=amount1, id=None)[0]
        transaction2 = transaction_factory(wallet=self.wallet, obj_num=1,
                                           amount=amount2, id=None)[0]

        transaction1.save()

        with self.assertRaises(ValidationError):
            transaction2.save()

        self.wallet.refresh_from_db()
        self.assertEqual(amount1, self.wallet.balance)

    def test_delete(self):
        """Transaction can not be deleted"""
        amount = ext_decimal(start=0.0, end=1000.0)
        transaction = transaction_factory(wallet=self.wallet, obj_num=1,
                                          id=None, amount=amount)[0]
        transaction.save()

        with self.assertRaises(ValidationError):
            transaction.delete()

    def test_edit(self):
        """Transaction can not be edited"""
        amount = ext_decimal(start=0.0, end=1000.0)
        transaction = transaction_factory(wallet=self.wallet, obj_num=1,
                                          id=None, amount=amount)[0]
        transaction.save()
        transaction.amount = -1

        with self.assertRaises(ValidationError):
            transaction.save()
