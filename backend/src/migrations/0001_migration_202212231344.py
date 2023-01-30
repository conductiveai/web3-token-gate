# auto-generated snapshot
from peewee import *
import datetime
import models.common
import peewee
import playhouse.postgres_ext
import uuid


snapshot = Snapshot()


@snapshot.append
class Chain(peewee.Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=128)
    class Meta:
        table_name = "chain"


@snapshot.append
class Contract(peewee.Model):
    address = models.common.Web3AddressField(max_length=42)
    token_name = CharField(max_length=128)
    erc_standard = IntegerField()
    holders = IntegerField()
    chain = snapshot.ForeignKeyField(index=True, model='chain')
    decimals = IntegerField()
    class Meta:
        table_name = "contract"


@snapshot.append
class Organization(peewee.Model):
    name = CharField(max_length=128)
    status = IntegerField(default=1)
    created_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    updated_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    class Meta:
        table_name = "organization"


@snapshot.append
class Wallet(peewee.Model):
    address = models.common.Web3AddressField(max_length=42)
    chain = snapshot.ForeignKeyField(index=True, model='chain')
    is_super_admin = BooleanField(default=False)
    verified_at = playhouse.postgres_ext.DateTimeTZField(null=True)
    created_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    updated_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    class Meta:
        table_name = "wallet"


@snapshot.append
class OrganizationAdmin(peewee.Model):
    organization = snapshot.ForeignKeyField(index=True, model='organization')
    wallet = snapshot.ForeignKeyField(index=True, model='wallet')
    status = IntegerField(default=1)
    created_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    updated_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    class Meta:
        table_name = "organizationadmin"


@snapshot.append
class OrganizationContract(peewee.Model):
    uuid = CharField(default=uuid.uuid4, max_length=36, unique=True)
    threshold = IntegerField(default=1)
    organization = snapshot.ForeignKeyField(index=True, model='organization')
    contract = snapshot.ForeignKeyField(index=True, model='contract')
    status = IntegerField(default=1)
    token_id_whitelist = playhouse.postgres_ext.JSONField(default=[])
    texts = playhouse.postgres_ext.JSONField(default={})
    title = CharField(max_length=50, null=True)
    image = TextField(null=True)
    created_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    updated_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    class Meta:
        table_name = "organizationcontract"


@snapshot.append
class Profile(peewee.Model):
    context = snapshot.ForeignKeyField(index=True, model='organizationcontract')
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    email = CharField(max_length=128)
    phone = CharField(max_length=128)
    country = CharField(max_length=128)
    address1 = CharField(max_length=30)
    address2 = CharField(max_length=30)
    address3 = CharField(max_length=30, null=True)
    city = CharField(max_length=128)
    region = CharField(max_length=128)
    postal_code = CharField(max_length=16)
    message = CharField(max_length=1000, null=True)
    wallet = snapshot.ForeignKeyField(backref='profiles', index=True, model='wallet')
    sizes = playhouse.postgres_ext.JSONField(default=[])
    status = SmallIntegerField(default=1)
    created_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    updated_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    class Meta:
        table_name = "profile"
        indexes = (
            (('context_id', 'wallet_id'), True),
            )


@snapshot.append
class Transaction(peewee.Model):
    chain = snapshot.ForeignKeyField(index=True, model='chain')
    contract = snapshot.ForeignKeyField(index=True, model='contract')
    block_number = IntegerField()
    timestamp = playhouse.postgres_ext.DateTimeTZField()
    hash = models.common.Web3HashField(max_length=66)
    nonce = IntegerField()
    block_hash = models.common.Web3HashField(max_length=66)
    index = IntegerField()
    from_address = models.common.Web3AddressField(max_length=42)
    to_address = models.common.Web3AddressField(max_length=42)
    gas = BigIntegerField()
    gas_price = BigIntegerField()
    gas_used = BigIntegerField()
    cumulative_gas_used = BigIntegerField()
    token_id = DecimalField(auto_round=False, decimal_places=0, max_digits=78, rounding='ROUND_HALF_EVEN', null=True)
    value = DecimalField(auto_round=False, decimal_places=0, max_digits=78, null=True, rounding='ROUND_HALF_EVEN')
    confirmations = BigIntegerField()
    created_at = playhouse.postgres_ext.DateTimeTZField(default=datetime.datetime.now)
    class Meta:
        table_name = "transaction"


