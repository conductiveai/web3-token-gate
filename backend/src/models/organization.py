from __future__ import annotations


import datetime

from typing import List, Optional, Dict, Union
from uuid import UUID, uuid4

from peewee import CharField, ForeignKeyField, IntegerField, TextField
from playhouse.postgres_ext import DateTimeTZField, JSONField

from database import BaseModel
from models.contract import Contract
from models.wallet import Wallet
from schemas.organization import Breakdown


class Organization(BaseModel):
    """ An organization that may have multiple contracts and verification links associated """

    class Status:
        ACTIVE = 1
        DELETED = 0

    name = CharField(max_length=128)
    status = IntegerField(default=Status.ACTIVE)

    created_at = DateTimeTZField(default=datetime.datetime.now)
    updated_at = DateTimeTZField(default=datetime.datetime.now)

    def is_admin(self, wallet: Wallet) -> bool:
        """ Check whether wallet is administrator of this organization

            Args:
                wallet - wallet to check

            Returns:
                whether wallet is administrator or not
        """
        return self.is_address_admin(wallet.address)

    @property
    def contracts(self) -> List[Contract]:
        """ A view on many-to-many relation, including some organization-specific fields on contract rows

            Returns:
                contracts associated with this organization with additional fields
        """
        from models.contract import Contract

        items = list(Contract.select(
            Contract,
            OrganizationContract.uuid.alias('context_uuid'),
            OrganizationContract.threshold,
            OrganizationContract.title,
            OrganizationContract.image,
        ).join(OrganizationContract).where(
            OrganizationContract.organization == self,
            OrganizationContract.status == OrganizationContract.Status.ACTIVE
        ).objects(Contract))

        return items

    @property
    def contexts(self) -> List[OrganizationContract]:
        """ List of contexts existing in this organization.

            Returns:
                OrganizationContract instances in this organization
        """
        return list(OrganizationContract.select().where(
            OrganizationContract.organization == self,
            OrganizationContract.status == OrganizationContract.Status.ACTIVE
        ))

    @property
    def admins(self) -> List[Wallet]:
        """ All administrators of this organization

            Returns:
                wallets that have administrative permissions
        """
        return list(Wallet.select().join(OrganizationAdmin).where(
            OrganizationAdmin.organization == self,
            OrganizationAdmin.status == OrganizationAdmin.Status.ACTIVE
        ))

    def get_tx_breakdowns(self) -> List[Breakdown]:
        """ Transactions within last 30 days grouped by day for each contract

            Returns:
                list of breakdowns for each contract in this organization
        """
        return [
            contract.get_tx_breakdowns() for contract in self.contracts
        ]

    def get_wallet_breakdowns(self) -> List[Breakdown]:
        """ Wallets within last 30 days grouped by day for each contract

            Returns:
                list of breakdowns for each profile in this organization
        """
        return [
            contract.get_wallet_breakdowns(self) for contract in self.contracts
        ]

    def count_transactions(self, days):
        """ Count transactions in this organization (sum of transactions for contracts associated)

            Args:
                days - how far back to go

            Returns:
                transaction count across possibly multiple contracts
        """
        return sum([
            contract.count_transactions(days) for contract in self.contracts
        ])

    def count_users(self, days):
        """ Count users (profiles) that were created in this organization

            Args:
                days - how far back to go

            Returns:
                user count
        """
        return sum([
            contract.count_users(self, days) for contract in self.contracts
        ])

    def add_admin(self, wallet: Wallet):
        """ Add admin to this organization

            Args:
                wallet - wallet of administrator to add
        """
        OrganizationAdmin.get_or_create(
            organization=self,
            wallet=wallet,
            status=OrganizationAdmin.Status.ACTIVE
        )

    def add_contract(
            self,
            contract: Contract,
            threshold: int = 1,
            token_id_whitelist: List[int] = None,
            title: Optional[str] = None,
            image: Optional[str] = None,
            texts: Optional[Dict[str, str]] = None,
    ) -> Contract:
        """ Add contract to this organization

        Args:
            contract - contract to add
            threshold - amount of contract tokens user must hold in order to participate
            token_id_whitelist - list of whitelisted token IDs, that allow access to gated content. Ignored if empty
            title - redemption form title
            image - redemption form image
            texts - text items that will be displayed on redemption form

        Returns:
            Contract instance instrumented with additional organization specific fields
        """
        org_contract = OrganizationContract.create(
            organization=self,
            contract=contract,
            threshold=threshold,
            status=OrganizationContract.Status.ACTIVE,
            token_id_whitelist=token_id_whitelist or [],
            title=title or None,
            image=image,
            texts=texts or {}
        )
        return org_contract.get_contract()

    def remove_admin(self, wallet: Wallet):
        """ Remove admin from this organization

            Args:
                wallet - admin to remove
        """
        OrganizationAdmin.update(status=OrganizationAdmin.Status.DELETED).where(
            OrganizationAdmin.organization == self,
            OrganizationAdmin.wallet == wallet
        ).execute()

    def is_address_admin(self, address: str) -> bool:
        """ Check if address has administrative permissions in this organization.

            Args:
                address: wallet address
            Returns:
                whether address is admin of this organization or not
        """
        return OrganizationAdmin.select().join(Wallet).where(
            OrganizationAdmin.organization == self,
            Wallet.address == address,
            OrganizationAdmin.status == OrganizationAdmin.Status.ACTIVE
        ).exists()


class OrganizationAdmin(BaseModel):
    """ Helper model linking wallet with administrative permissions to organization """

    class Status:
        ACTIVE = 1
        DELETED = 0

    organization = ForeignKeyField(Organization)
    wallet = ForeignKeyField(Wallet)
    status = IntegerField(default=Status.ACTIVE)

    created_at = DateTimeTZField(default=datetime.datetime.now)
    updated_at = DateTimeTZField(default=datetime.datetime.now)


class OrganizationContract(BaseModel):
    """ Helper model linking organization to associated contract. Also serves as 'context';
        Each organization contract (context from now on) holds additional data specific to
        organization and contract combination, such as token_id_whitelist, title, image, texts.
        Each context will have its own verification URL, and such URLs of same organization will
        be seemingly unrelated to the end user.

        **NOTE** Same contract may be registered multiple times even within same organization.
        Organization + contract pair does not uniquely identify a context. Use UUID of context instead.
    """
    class Status:
        ACTIVE = 1
        DELETED = 0

    uuid = CharField(max_length=36, unique=True, default=uuid4)
    threshold = IntegerField(default=1)

    organization = ForeignKeyField(Organization)
    contract = ForeignKeyField(Contract)
    status = IntegerField(default=Status.ACTIVE)

    token_id_whitelist = JSONField(default=[])
    title = CharField(max_length=50, null=True)
    image = TextField(null=True)
    texts = JSONField(default={})

    created_at = DateTimeTZField(default=datetime.datetime.now)
    updated_at = DateTimeTZField(default=datetime.datetime.now)

    @classmethod
    def get_by_uuid(cls, uuid: Union[str, UUID]) -> Optional[OrganizationContract]:
        """
            Get context by its uuid

            Args:
                uuid - uuid to get context by

            Returns:
                Context if exists
        """
        return cls.get_or_none(cls.uuid == uuid, cls.status == cls.Status.ACTIVE)

    def get_profiles(self):
        """ All profiles in this context

        Returns:
            query getting all profiles within this context
        """
        from models.profile import Profile

        return Profile.select().where(Profile.context == self)

    def get_contract(self) -> Contract:
        """ Get contract from this context

        Returns:
            instrumented contract instance from this context
        """
        return Contract.select(
            Contract,
            OrganizationContract.uuid.alias('context_uuid'),
            OrganizationContract.threshold,
            OrganizationContract.title,
            OrganizationContract.image,
        ).join(OrganizationContract).where(
            Contract.id == self.contract.id
       ).get()

    def update_context(self, **data):
        """ Update this context

        Args:
            data - fields to update context with
        """
        OrganizationContract.update(**data).where(OrganizationContract.id == self.id).execute()

    def deactivate(self):
        """ Change status of context to DELETED """
        self.status = OrganizationContract.Status.DELETED
        self.save()
