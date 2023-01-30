from fastapi import Depends

from exceptions.exceptions import ApiError
from services.user import UserService, UserServiceType


def _get_superadmin(user_service: UserServiceType = UserService) -> UserServiceType:
    wallet = user_service.auth_service.get_wallet()

    if not wallet.is_super_admin:
        raise ApiError('You are not a super admin')

    return user_service


GetSuperAdmin = Depends(_get_superadmin)
