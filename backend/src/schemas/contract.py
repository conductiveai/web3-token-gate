from typing import Optional

from pydantic import BaseModel, validator, AnyUrl
from uuid import UUID

from models.chain import Chain
from schemas.common import Web3Address


class Contract(BaseModel):
    id: int
    token_name: str
    address: Web3Address
    context_uuid: Optional[UUID]
    threshold: Optional[int]
    title: Optional[str]
    image: Optional[AnyUrl]

    class Config:
        orm_mode = True


class CreateContractRequest(BaseModel):
    address: Web3Address
    chain: int

    @validator('chain')
    def chain_exists(cls, v):
        if not Chain.get_or_none(id=v):
            raise ValueError('Chain does not exist')
        return v
