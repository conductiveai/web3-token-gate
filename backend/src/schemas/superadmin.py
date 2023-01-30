from typing import List, Optional

from pydantic import BaseModel, validator, Field

from schemas.common import Web3Address


class CreateOrganizationRequest(BaseModel):
    name: str
    contracts: List[int]
    admins: List[Web3Address]

    @validator('contracts')
    def validate_contracts(cls, v):
        from models.contract import Contract

        contracts = []

        for contract_id in set(v):
            contract = Contract.get_or_none(id=contract_id)
            if not contract:
                raise ValueError(f'Contract {contract_id} does not exist')

            contracts.append(contract_id)

        return contracts
