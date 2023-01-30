import datetime
import logging
from typing import List

from adapters.blockscan import Blockscan
from models.contract import Contract
from models.organization import OrganizationContract
from models.transaction import Transaction
from schemas.blockscan import BlockScanTransaction


def process_contracts():
    """ Process all contracts """

    for contract in Contract.select().join(OrganizationContract).where(
            OrganizationContract.status == OrganizationContract.Status.ACTIVE
    ).distinct():
        process_contract(contract)


def process_contract(contract: Contract):
    """ Save new transactions for given contract

    Args:
        contract - contract to process
    """

    bulk: List[BlockScanTransaction] = []

    for transaction in Blockscan.get_transactions(contract):
        bulk.append(transaction)
        if len(bulk) >= 1000:
            logging.info(f'Saving bulk of {len(bulk)} transactions')
            save_transactions(transactions=bulk, contract=contract)
            bulk.clear()

    if bulk:
        logging.info(f'Saving {len(bulk)} leftover transactions')
        save_transactions(transactions=bulk, contract=contract)


def save_transactions(transactions: List[BlockScanTransaction], contract: Contract):
    """ Save bulk of transactions for given contract into the database in one operation

    Args:
        transactions - transactions to save
        contract - contract to save transactions for
    """
    rows = []

    logging.info(f'Saving transactions...')

    for transaction in transactions:
        rows.append({
            'chain': contract.chain,
            'contract': contract,
            'block_number': transaction.block_number,
            'timestamp': datetime.datetime.fromtimestamp(transaction.timestamp, tz=datetime.timezone.utc),
            'hash': transaction.hash,
            'nonce': transaction.nonce,
            'block_hash': transaction.block_hash,
            'index': transaction.transaction_index,
            'from_address': transaction.from_address,
            'to_address': transaction.to_address,
            'value': transaction.get_value(),
            'gas': transaction.gas,
            'gas_price': transaction.gas_price,
            'gas_used': transaction.gas_used,
            'cumulative_gas_used': transaction.cumulative_gas_used,
            'token_id': transaction.token_id,
            'confirmations': transaction.confirmations,
        })

    count_before = Transaction.select().count()
    Transaction.insert_many(rows).execute()
    count_after = Transaction.select().count()
    logging.info(f'Inserted {count_after - count_before} new transactions out of {len(rows)} total')
