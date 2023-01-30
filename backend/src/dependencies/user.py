from typing import Optional

import jwt
from fastapi import Depends
from starlette.requests import Request

from exceptions.exceptions import ApiError
from models.chain import Chain
from models.organization import OrganizationContract, Organization
from models.profile import Profile
from models.wallet import Wallet
from settings import settings


class AuthServiceType:
    """ FastAPI dependency decoding JWT and providing access to user functions """

    def __init__(self, token):
        if not token:
            raise ApiError('JWT is required')

        self.token = token

        try:
            decoded = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise ApiError('Invalid signature')
        except jwt.exceptions.ExpiredSignatureError:
            raise ApiError('JWT is expired')
        except jwt.exceptions.DecodeError:
            raise ApiError('Invalid JWT')

        for field in {'wallet_address'}:
            if field not in decoded:
                raise ApiError('Invalid JWT payload')

        self._wallet_address = decoded['wallet_address']

        wallet = self.get_wallet()

        if wallet is None:
            raise ApiError('Wallet does not exist')

    def get_profile(self, context: OrganizationContract) -> Optional[Profile]:
        """ Get profile of this user in given context if exists

            Args:
                context - context to get profile in

            Returns:
                Profile if exists
        """
        return Profile.select().join(Wallet).where(
            Wallet.address == self._wallet_address,
            Profile.context == context
        ).get_or_none()

    def get_wallet(self, chain: Chain = None, or_create=False) -> Optional[Wallet]:
        """ Get wallet object belonging to this user.

            Args:
                chain - chain on which to get the wallet instance
                or_create - whether to create a wallet if it wasn't found

            Returns:
                wallet if exists or was created
        """
        if chain:
            wallet = Wallet.select().filter(
                address=self._wallet_address,
                chain=chain
            ).get_or_none()
        else:
            wallet = Wallet.get_or_none(
                address=self._wallet_address
            )

        if wallet is None and or_create:
            wallet = Wallet.create(
                address=self._wallet_address,
                chain=chain or 1
            )

        return wallet

    def is_super_admin(self) -> bool:
        """ Whether this user is superadmin

        Returns:
            is superadmin
        """
        return Wallet.select().filter(address=self._wallet_address, is_super_admin=True).exists()


def auth_service_dependency(request: Request, token: Optional[str] = None) -> AuthServiceType:
    """ Get user from JWT token """
    token = request.headers.get('Authorization', token)
    return AuthServiceType(token=token)


AuthService = Depends(auth_service_dependency)
