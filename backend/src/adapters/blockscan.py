import logging
import traceback
from typing import Tuple, Generator, Optional

import requests

from models.chain import Chain
from models.contract import Contract
from models.transaction import Transaction
from schemas.blockscan import BlockScanTransaction, TokenInfo
from settings import settings


class Blockscan:
    """ Blockscan API adapter """

    @classmethod
    def _get_url_and_key(cls, chain: Chain) -> Tuple[str, str]:
        if chain.id == 1:
            return 'https://api.etherscan.io/api', settings.etherscan_api_key.get_secret_value()
        elif chain.id == 56:
            return 'https://api.bscscan.com/api', settings.bscscan_api_key.get_secret_value()
        elif chain.id == 137:
            return 'https://api.polygonscan.com/api', settings.polygon_api_key.get_secret_value()
        else:
            raise ValueError('Invalid chain name')

    @classmethod
    def _get_latest_block(cls, contract: Contract):
        return Transaction.select(Transaction.block_number).where(
            Transaction.contract == contract
        ).order_by(
            Transaction.block_number.desc()
        ).limit(1).scalar() or 0

    @classmethod
    def get_transactions(cls, contract: Contract) -> Generator[BlockScanTransaction, None, None]:

        url, api_key = cls._get_url_and_key(contract.chain)
        logging.info(f'Get Transactions for {contract.token_name} ({contract.address} on {contract.chain.name})')

        if contract.erc_standard == 20:
            action_type = 'tokentx'
        elif contract.erc_standard == 721:
            action_type = 'tokennfttx'
        elif contract.erc_standard == 1155:
            action_type = 'token1155tx'
        else:
            raise ValueError('Invalid contract type')

        params = {
            'module': 'account',
            'action': action_type,
            'contractaddress': contract.address,
            'sort': 'asc',
            'offset': 5000,  # 10k is maximum, but might cause timeouts
            'apikey': api_key,
            'page': 1,
            'endblock': 'latest'
        }

        latest_block = cls._get_latest_block(contract)
        while True:

            params['startblock'] = latest_block + 1
            logging.info(f'Latest block: {latest_block}')
            r = requests.get(url, params=params)
            items = r.json()['result']

            if not items:
                logging.info(f'No more items: {r.text}')
                break

            logging.info(f'Got {len(items)} items')

            items = [BlockScanTransaction(**item) for item in items]
            new_latest_block = max(items, key=lambda x: x.block_number).block_number

            logging.info(f'Latest block from received transactions: {new_latest_block}')

            yield from items

            if new_latest_block == latest_block and len(items) == params['offset']:
                logging.warning(
                    f'Block has more transactions than data window is capable of returning. '
                    f'To avoid infinite loop contract {contract.address} will be skipped'
                )
                break

            latest_block = new_latest_block

    @classmethod
    def get_info(cls, contract_address: str, chain: Chain) -> Optional[TokenInfo]:
        url, api_key = cls._get_url_and_key(chain)

        params = {
            'module': 'token',
            'action': 'tokeninfo',
            'contractaddress': contract_address,
            'apikey': api_key,
        }

        r = requests.get(url, params=params)

        data = r.json()

        if data['status'] != '1':
            logging.info(data)
            raise ValueError(data['message'])

        try:
            return TokenInfo(**r.json()['result'][0])
        except Exception:
            traceback.print_exc()
            return None

