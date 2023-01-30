from peewee import ForeignKeyField, DecimalField
from playhouse.postgres_ext import DateTimeTZField

from database import BaseModel
from models.chain import Chain
from models.common import Web3AddressField
from models.contract import Contract


class Balance(BaseModel):
    """ A materialized view of balance of a wallet on a chain """

    address = Web3AddressField()
    chain = ForeignKeyField(Chain)
    contract = ForeignKeyField(Contract)
    balance = DecimalField(decimal_places=0, max_digits=78, null=True)
    token_id = DecimalField(decimal_places=0, max_digits=78, null=True)
    date = DateTimeTZField()

    class Meta:
        table_name = 'wallet_balances'
