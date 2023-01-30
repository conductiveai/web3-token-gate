from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Optional, List

from peewee import IntegerField, ForeignKeyField, fn, CharField

from adapters.contractdetector import ContractDetector, AddressType
from database import BaseModel
from exceptions.exceptions import ApiError
from models.chain import Chain
from models.common import Web3AddressField
from schemas.organization import Breakdown, BreakdownItem
from settings import settings
from utils import fill_breakdown


class Contract(BaseModel):
    """ A smart contract on a chain """

    address: str = Web3AddressField()
    token_name: str = CharField(max_length=128)
    erc_standard: int = IntegerField()
    holders: int = IntegerField()
    chain = ForeignKeyField(Chain)
    decimals = IntegerField()

    def get_tx_breakdowns(self) -> Breakdown:
        """ return transactions within last 30 days grouped by day """

        from models.transaction import Transaction

        items = Transaction.select(
            fn.DATE(Transaction.timestamp).alias('label'),
            fn.COUNT('*').alias('count')
        ).where(
            Transaction.contract == self,
            Transaction.timestamp > datetime.now() - timedelta(days=30)
        ).group_by(
            fn.DATE(Transaction.timestamp)
        ).dicts()

        return Breakdown(
            key=self.token_name,
            items=fill_breakdown([BreakdownItem(**item) for item in items])
        )

    @classmethod
    def get_or_init(cls, address: str, chain: Chain) -> Contract:
        """ Get or create contract. If created, metadata will be fetched from blockscan and rpc node if needed.

            Args:
                address - Contract address
                chain - Contract chain

            Returns:
                created or existing contract
        """

        # check if contract already exists
        contract = Contract.get_or_none(Contract.address == address, Contract.chain == chain)

        if contract:
            return contract

        from adapters.blockscan import get_info

        # get contract metadata from blockscan
        info = get_info(address, chain)

        if not info:
            raise ApiError(f'Contract {address} not found on chain {chain}')

        standard = info.get_erc_standard()

        # blockscan didn't provide erc standard data
        if not standard:
            logging.info("Get contract type from contract detector")

            # use contract detector for erc type detection
            detector = ContractDetector(settings.rpc_endpoints)

            address_type = detector.get_address_type(address, chain)
            logging.info(f"Detection: {address_type}")

            if address_type == AddressType.ERC_20_CONTRACT:
                standard = 20
            elif address_type == AddressType.ERC_721_CONTRACT:
                standard = 721
            elif address_type == AddressType.ERC_1155_CONTRACT:
                standard = 1155
            else:
                raise ApiError(f'Could not detect contract type for {address} on {chain}')

        return Contract.create(
            address=address,
            chain=chain,
            holders=0,
            erc_standard=standard,
            token_name=info.name,
            decimals=info.divisor,
        )

    def get_wallet_breakdowns(self, organization) -> Breakdown:
        """ Get breakdown of profile creation for this contract within organization by day.

        Args:
            organization - organization which has this contract and in which profiles were created.

        Returns:
            Breakdown object with token name as key, profile creation date as label,
            and profile count as count on BreakdownItem.
        """
        from models.profile import Profile
        from models.organization import OrganizationContract

        items = Profile.select(
            fn.DATE(Profile.created_at).alias('label'),
            fn.COUNT('*').alias('count')
        ).join(OrganizationContract).where(
            OrganizationContract.contract == self,
            OrganizationContract.organization == organization,
            Profile.created_at > datetime.now() - timedelta(days=30)
        ).group_by(
            fn.DATE(Profile.created_at)
        ).dicts()
        return Breakdown(
            key=self.token_name,
            items=fill_breakdown([BreakdownItem(**item) for item in items])
        )

    def count_transactions(self, days) -> int:
        """ Count transactions for this contract within last N days

            Args:
                days - how far back to go

            Returns:
                transaction count
        """
        from models.transaction import Transaction

        return Transaction.select().where(
            Transaction.contract == self,
            Transaction.timestamp > datetime.now() - timedelta(days=days)
        ).count()

    def count_users(self, organization, days) -> int:
        """ Count confirmed users of organization that connected their wallet, proving they hold this contract

        Args:
            organization - organization that has this contract
            days - how far back to go

        Returns:
            user count
        """
        from models.profile import Profile
        from models.organization import OrganizationContract

        return Profile.select().join(OrganizationContract).where(
            OrganizationContract.contract == self,
            OrganizationContract.organization == organization,
            Profile.created_at > datetime.now() - timedelta(days=days)
        ).count()
