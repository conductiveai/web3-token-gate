from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field

from schemas.context import Context
from schemas.organization import Organization
from schemas.profile import Profile, SizeData
from schemas.wallet import Wallet


class User(BaseModel):
    wallet: Wallet
    context: Optional[Context]
    is_super_admin: bool
    organizations: List[Organization]


class UserContext(BaseModel):
    balance: float
    relevant_balance: float
    profile: Optional[Profile]


class CreateProfile(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    country: str
    address1: str = Field(None, max_length=30)
    address2: str = Field(None, max_length=30)
    address3: Optional[str] = Field(None, max_length=30)
    city: str
    region: str
    postal_code: str
    message: Optional[str]
    sizes: List[SizeData]


class TokenBalance(BaseModel):
    token_id: int
    balance: float

    class Config:
        orm_mode = True
