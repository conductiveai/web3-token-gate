import hashlib
from typing import Optional

from fastapi import APIRouter

from database import db
from exceptions.exceptions import ApiError
from models.contract import Contract
from schemas.common import ResponseSchema
from services.contract import process_contracts, process_contract
from settings import settings

router = APIRouter()


@router.post("/{api_key}", response_model=ResponseSchema[str])
def process_contract(api_key: str, contract_id: Optional[int] = None):
    """ Process contract. Processing includes fetching transactions from blockscan and saving them to the database,
        then wallet_balances materialized view will get refreshed, as well as holder count will be updated on contracts.

        Args:
            api_key - hash of application secret key concatenated with a prefix.
            contract_id - optional contract id to refresh a single contract instead of all contracts.
    """

    # compute expected api_key
    to_hash = f'APP_SECRET_KEY-{settings.secret_key.get_secret_value()}'.encode('utf-8')
    computed_api_key = hashlib.sha256(to_hash).hexdigest()

    # compare keys
    if api_key != computed_api_key:
        raise ApiError('Invalid API key')

    if contract_id is not None:
        # refresh single contract
        contract = Contract.get_or_none(Contract.id == contract_id)

        if contract is None:
            raise ApiError('Contract not found')

        process_contract(contract)
    else:
        # refresh all contracts
        process_contracts()

    # update materialized views and count fields
    db.execute_sql('refresh materialized view concurrently "public"."wallet_balances";')
    db.execute_sql("""
        UPDATE contract set holders = t.holders from (
            select contract_id, count(*) as holders from transaction group by contract_id
        ) t 
        where contract.id = t.contract_id;
    """)

    return ResponseSchema(error=False, data="", message='Contracts processed')
