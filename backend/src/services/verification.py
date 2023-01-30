import datetime
import hashlib
import re
from typing import Optional

import pytz
import jwt

from exceptions.exceptions import ApiError
from models.wallet import Wallet
from settings import settings
from web3.auto import w3
from eth_account.messages import defunct_hash_message


def recover_address(message, signature):
    message_hash = defunct_hash_message(text=message)
    address = w3.eth.account.recoverHash(message_hash, signature=signature)
    return address


class VerificationService:
    """ Service managing wallet verification by generating message to be signed
        and verifying signature afterwards
    """

    @classmethod
    def get_message(cls, address: str, expires_at: int):
        msg_hash = cls.get_message_hash(address, expires_at)
        return f"Please sign this message to verify your address: {msg_hash}.{expires_at}"

    @classmethod
    def get_message_hash(cls, address: str, expires_at: int):
        secret = settings.secret_key.get_secret_value()
        msg = f"{address}.{secret}.{expires_at}"
        msg_hash = hashlib.sha256(msg.encode("utf-8")).hexdigest()
        return msg_hash

    @classmethod
    def verify(cls, wallet_address: str, signature: str, message: str) -> Optional[Wallet]:
        match = re.match(r'.*(s*[a-f0-9]{64})\.([0-9]{10})', message)

        if not match:
            raise ApiError("Invalid message")

        msg_hash = match.group(1)
        expires_at = int(match.group(2))

        if msg_hash != cls.get_message_hash(wallet_address, expires_at):
            raise ApiError("Invalid signature")

        if expires_at < int(datetime.datetime.now(tz=pytz.utc).timestamp()):
            raise ApiError("Signature expired")

        recovered_address = recover_address(message, signature)

        if not recovered_address.lower() == wallet_address.lower():
            return None

        wallet, _ = Wallet.get_or_create(
            address=wallet_address,

            defaults={
                "verified_at": datetime.datetime.now(tz=pytz.utc),
                "chain_id": 1,
            }
        )
        return wallet

    @classmethod
    def create_jwt(cls, wallet_address):

        token = jwt.encode(
            {
                "wallet_address": wallet_address,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            },
            settings.secret_key.get_secret_value(),
            algorithm="HS256",
        )

        return token
