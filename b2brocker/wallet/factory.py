import random
from decimal import Decimal

from mimesis import Field, Locale, Schema

from .models import Wallet, Transaction

# For fixed faker_seed change by manual
# For simplicity in implementing the factory with random data generation,
# this part of the code is fixed
faker_seed = random.randint(1, 10000)
print('-' * 40)
print(f">>> FAKER_SEED: {faker_seed}")
print('-' * 40)
mf = Field(locale=Locale.EN, seed=faker_seed)
pseudo_random = random.Random(faker_seed)


def ext_decimal(
        start: float = -1000.0,
        end: float = 1000.0,
        decimal_places: int = 18
) -> Decimal:
    n = pseudo_random.uniform(start, end)
    decimal_value = Decimal(str(n))
    format_string = '1.' + '0' * decimal_places
    return decimal_value.quantize(Decimal(format_string))


def wallet_factory(obj_num=1, **fields):
    """
    The factory creates a Wallet with random data
    :param obj_num: number of objects
    :param fields: hard-set fields
    """
    schema_definition = lambda: {
        'id': mf('increment'),
        'label': mf('name'),
        'balance': ext_decimal(start=0.0, end=1000.0)
    }
    schema = Schema(schema=schema_definition, iterations=obj_num)
    data_set = schema.create()
    obj_set = []
    for data_raw in data_set:
        data = {
            **data_raw,
            **fields,
        }
        obj = Wallet(**data)
        obj_set.append(obj)
    return obj_set


def transaction_factory(wallet, obj_num=1, **fields):
    """
    The factory creates a Transaction with random data
    :param obj_num: number of objects
    :param fields: hard-set fields
    """
    schema_definition = lambda: {
        'id': mf('increment'),
        'txid': mf('uuid'),
        'amount': ext_decimal(start=-1000.0, end=1000.0)
    }
    schema = Schema(schema=schema_definition, iterations=obj_num)
    data_set = schema.create()
    obj_set = []
    for data_raw in data_set:
        data = {
            **data_raw,
            **fields,
        }
        obj = Transaction(**data, wallet=wallet)
        obj_set.append(obj)
    return obj_set
