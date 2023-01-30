from typing import Optional
from uuid import UUID

from fastapi import Depends

from exceptions.exceptions import ApiError
from models.organization import Organization, OrganizationContract
from services.user import UserService, UserServiceType


def GetOrganization(required=True):  # NOQA
    """ FastAPI dependency to get organization by ID.

        Args:
            required: whether organization is required

        Returns:
            'Depends' object
    """
    def _get_organization(org_id: Optional[int] = None):

        if not org_id:
            if required:
                raise ApiError('org_id is required')
            else:
                return None

        org = Organization.get_or_none(
            id=org_id
        )

        if not org:
            raise ApiError('Organization does not exist')

        return org

    return Depends(_get_organization)


def GetContext(required):  # NOQA
    """ FastAPI dependency to get context by UUID.

        Args:
            required: whether context is required

        Returns:
            'Depends' object
    """
    def _get_context(context_uuid: Optional[UUID] = None) -> Optional[OrganizationContract]:
        """ Wallets would usually make requests within context of organization contract.
            Wallet wants to prove is holds a particular contract,
            but this contract might be used by multiple organizations.
        """

        if not context_uuid:
            if not required:
                return None
            raise ApiError('Context is required')

        org_contract = OrganizationContract.get_by_uuid(context_uuid)

        if not org_contract:
            raise ApiError("Context not found")

        return org_contract

    return Depends(_get_context)


def _require_context(
        user_service: UserServiceType = UserService,
        context: OrganizationContract = GetContext(required=True),
):
    """ Require user to have admin access to requested context """

    if not user_service.has_access(context.organization):
        raise ApiError('You are not an admin of this organization')

    return context


RequireContext = Depends(_require_context)


def _require_organization(org_id: int, user_service: UserServiceType = UserService):
    org = Organization.get_or_none(
        id=org_id
    )

    if not org:
        raise ApiError('Organization does not exist')

    if not user_service.has_access(organization=org):
        raise ApiError('You do not have access to this organization')

    return org


RequireOrganization = Depends(_require_organization)
