from datetime import datetime, timedelta

import pytz as pytz
from fastapi import APIRouter


from schemas.common import ResponseSchema
from schemas.verification import SignableMessageRequest, VerificationRequest
from services.verification import VerificationService

router = APIRouter()


@router.post("/message", response_model=ResponseSchema[str])
def get_message(data: SignableMessageRequest):
    """ Generate message to sign """

    expires_at = int((datetime.now(tz=pytz.utc) + timedelta(minutes=5)).timestamp())

    return ResponseSchema(
        error=False,
        data=VerificationService.get_message(data.wallet_address, expires_at)
    )


@router.post("/verify", response_model=ResponseSchema[str])
def verify(data: VerificationRequest):
    """ Verify wallet by submitting signed message """

    wallet = VerificationService.verify(
        wallet_address=data.wallet_address,
        signature=data.signature,
        message=data.message,
    )

    if not wallet:
        return ResponseSchema(
            error=True,
            message="Invalid signature"
        )

    token = VerificationService.create_jwt(data.wallet_address)

    return ResponseSchema(
        error=False,
        message="Successfully verified",
        data=token
    )
