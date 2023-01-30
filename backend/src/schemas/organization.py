from typing import List, Any, Optional
from uuid import UUID

from pydantic import BaseModel, validator, PositiveInt, Field, AnyUrl

from schemas.common import Web3Address, ChainField
from schemas.context import Context
from schemas.contract import Contract
from schemas.wallet import Wallet


class Organization(BaseModel):
    id: int
    name: str
    admins: List[Wallet]
    contexts: List[Context]

    class Config:
        orm_mode = True


class BreakdownItem(BaseModel):
    label: Any
    count: int


class Breakdown(BaseModel):
    key: str
    items: List[BreakdownItem]


class CreateContractRequest(BaseModel):
    address: Web3Address
    chain: ChainField
    threshold: Optional[PositiveInt]
    token_id_whitelist: List[int]
    title: Optional[str]
    image: Optional[AnyUrl]


class AddAdminRequest(BaseModel):
    address: Web3Address


class RemoveAdminRequest(BaseModel):
    address: Web3Address


class UpdateContextRequest(BaseModel):
    threshold: Optional[PositiveInt]
    token_id_whitelist: List[int]
    title: Optional[str]
    image: Optional[AnyUrl]
    texts: Optional[dict]


class ContextWithOrg(Context):
    organization: Organization

    class Config:
        orm_mode = True
