from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=36, decimal_places=18, default=Decimal('0.0'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created', ]

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if self.balance < Decimal('0.0'):
            raise ValueError("Wallet balance cannot be negative")
        return super().save(*args, **kwargs)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created', ]

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("Editing transactions is not allowed")

        with (transaction.atomic()):
            transactions_qs = Transaction.objects.select_for_update() \
                .filter(wallet=self.wallet)
            wallet = Wallet.objects.select_for_update().get(pk=self.wallet.pk)

            balance = transactions_qs.aggregate(Sum('amount'))['amount__sum'] or 0
            balance += self.amount
            if balance < Decimal('0.0'):
                raise ValidationError("Resulting wallet balance cannot be negative")

            wallet.balance = balance
            wallet.save()
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Deleting transactions is not allowed")
