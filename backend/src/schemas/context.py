from typing import List, Optional, Dict
from uuid import UUID

from pydantic import BaseModel, AnyUrl

from schemas.contract import Contract


class Context(BaseModel):
    uuid: UUID
    threshold: int
    contract: Contract
    token_id_whitelist: List[int]
    title: Optional[str]
    image: Optional[AnyUrl]
    texts: Dict[str, str]

    class Config:
        orm_mode = True
