from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.chain import Chain
from schemas.common import Web3Address


class Wallet(BaseModel):
    address: Web3Address
    chain: Chain
    is_super_admin: bool
    verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

