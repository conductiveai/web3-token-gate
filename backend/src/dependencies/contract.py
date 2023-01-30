from fastapi import Depends

from exceptions.exceptions import ApiError
from models.contract import Contract


def _get_contract(contract_id: int):
    """ FastAPI dependency to get contract by ID """

    contract = Contract.get_or_none(id=contract_id)

    if not contract:
        raise ApiError('Contract does not exist')

    return contract


GetContract = Depends(_get_contract)
