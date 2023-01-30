from pydantic import BaseModel
from schemas.common import Web3Address


class VerificationRequest(BaseModel):
    wallet_address: Web3Address
    signature: str
    message: str


class SignableMessageRequest(BaseModel):
    wallet_address: Web3Address
