from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


from schemas.wallet import Wallet


class SizeData(BaseModel):
    token_id: int
    sizes: List[str]


class Profile(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    country: str
    address1: str
    address2: str
    address3: str
    city: str
    region: str
    postal_code: str
    message: Optional[str]
    status: int
    wallet: Wallet
    sizes: List[SizeData]

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
