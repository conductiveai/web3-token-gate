import datetime

from peewee import ForeignKeyField, IntegerField, TextField, DecimalField, BigIntegerField
from playhouse.postgres_ext import DateTimeTZField

from database import BaseModel
from models.chain import Chain
from models.common import Web3HashField, Web3AddressField
from models.contract import Contract


class Transaction(BaseModel):
    """ Blockchain transaction """

    chain = ForeignKeyField(Chain)
    contract = ForeignKeyField(Contract)
    block_number = IntegerField()
    timestamp = DateTimeTZField()
    hash = Web3HashField()
    nonce = IntegerField()
    block_hash = Web3HashField()
    index = IntegerField()
    from_address = Web3AddressField()
    to_address = Web3AddressField()
    gas = BigIntegerField()
    gas_price = BigIntegerField()
    gas_used = BigIntegerField()
    cumulative_gas_used = BigIntegerField()
    token_id = DecimalField(decimal_places=0, max_digits=78, null=True)
    value = DecimalField(decimal_places=0, max_digits=78, null=True)
    confirmations = BigIntegerField()

    created_at = DateTimeTZField(default=datetime.datetime.now)
