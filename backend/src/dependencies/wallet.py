from fastapi import Depends

from exceptions.exceptions import ApiError
from models.wallet import Wallet


def _get_wallet(wallet_id: int):
    wallet = Wallet.get_or_none(id=wallet_id)

    if not wallet:
        raise ApiError('Wallet does not exist')

    return wallet


GetWallet = Depends(_get_wallet)
