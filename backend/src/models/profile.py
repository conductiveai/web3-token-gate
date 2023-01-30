import datetime

from peewee import CharField, TextField, ForeignKeyField, SmallIntegerField
from playhouse.postgres_ext import DateTimeTZField, JSONField

from database import BaseModel
from models.organization import OrganizationContract
from models.wallet import Wallet


class Profile(BaseModel):
    """ User profile within a context """

    class Status:
        ACTIVE = 1
        DELETED = 0

    context = ForeignKeyField(OrganizationContract)

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
    wallet = ForeignKeyField(Wallet, backref='profiles')
    sizes = JSONField(default=[])
    status = SmallIntegerField(default=Status.ACTIVE)

    created_at = DateTimeTZField(default=datetime.datetime.now)
    updated_at = DateTimeTZField(default=datetime.datetime.now)
    
    class Meta:
        indexes = (
            (('context_id', 'wallet_id'), True),
        )
