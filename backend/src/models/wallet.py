import datetime

from peewee import ForeignKeyField, BooleanField
from playhouse.postgres_ext import DateTimeTZField

from database import BaseModel
from models.chain import Chain
from models.common import Web3AddressField


class Wallet(BaseModel):
    """ Blockchain wallet """

    address = Web3AddressField()
    chain = ForeignKeyField(Chain)
    is_super_admin = BooleanField(default=False)
    verified_at = DateTimeTZField(null=True)
    created_at = DateTimeTZField(default=datetime.datetime.now)
    updated_at = DateTimeTZField(default=datetime.datetime.now)

    def get_administrated_organizations(self):
        """ Organizations this wallet is an admin of

        Returns:
            query returning all organizations this wallet is admin of
        """
        from models.organization import Organization, OrganizationAdmin

        return Organization.select().join(OrganizationAdmin).where(
            OrganizationAdmin.wallet == self,
            OrganizationAdmin.status == OrganizationAdmin.Status.ACTIVE
        )
