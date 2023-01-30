from fastapi import Depends
from peewee import fn

from dependencies.user import AuthService, AuthServiceType
from exceptions.exceptions import ApiError
from models.balance import Balance

from models.organization import OrganizationContract, Organization, OrganizationAdmin
from models.profile import Profile
from schemas.user import User


class UserServiceType:
    """ Service on top of Authentication service providing high-level functionality """

    def __init__(self, auth_service):
        self.auth_service: AuthServiceType = auth_service

    def create_profile(self, context: OrganizationContract, **kwargs) -> Profile:
        """ Create a profile for user in given context

        Args:
            context - context to create profile in
            kwargs - profile fields

        Returns:
            created profile
        """

        wallet = self.auth_service.get_wallet(context.contract.chain, or_create=True)

        if Profile.select().where(
                Profile.wallet == wallet,
                Profile.context == context
        ).exists():
            raise ApiError('Profile already exists')

        kwargs['wallet'] = wallet
        kwargs['context'] = context

        return Profile.create(**kwargs)

    def update_profile(self, context: OrganizationContract, **kwargs) -> Profile:
        """ Update profile

            Args:
                context - context profile in which to update
                kwargs - fields to update

            Returns:
                updated profile
        """

        profile = self.auth_service.get_profile(context)

        if not profile:
            raise ApiError('Profile does not exist')

        Profile.update(**kwargs).where(Profile.id == profile.id).execute()
        return Profile.get_by_id(profile.id)

    def get_profile(self, context: OrganizationContract) -> Profile:
        """ Get profile in context if exists

            Args:
                context - context to get profile in

            Returns:
                profile if exists
        """

        return self.auth_service.get_profile(context)

    def get_balance(self, context: OrganizationContract, only_relevant: bool = False) -> int:
        """ Get wallet balance of given contract. If it is erc1155, return sum across all token ids

        Args:
            context - context to get balance for
            only_relevant - only return balance of whitelisted tokens. If whitelist is empty, equal to total balance.

        Returns:
            token balance
        """

        q = Balance.select(
            fn.SUM(Balance.balance)
        ).where(
            Balance.address == self.auth_service.get_wallet().address,
            Balance.contract == context.contract,
        ).group_by(
            Balance.address,
            Balance.contract
        )

        if only_relevant and context.token_id_whitelist:
            q = q.where(Balance.token_id.in_(context.token_id_whitelist))

        balance = q.scalar()

        decimals = context.contract.decimals

        balance = balance or 0

        return balance / 10 ** decimals

    def has_access(self, organization: Organization):
        """ Whether user has access to organization

        Args:
            organization - organization user trying to access

        Returns:
            whether user has access
        """
        if self.is_super_admin():
            return True

        return OrganizationAdmin.select().where(
            OrganizationAdmin.wallet == self.auth_service.get_wallet(),
            OrganizationAdmin.organization == organization,
            OrganizationAdmin.status == OrganizationAdmin.Status.ACTIVE
        ).exists()

    def get_me(self) -> User:
        """ Gather user data into one object

            Returns:
                user
        """
        return User(
            wallet=self.auth_service.get_wallet(),
            is_super_admin=self.is_super_admin(),
            organizations=list(self.auth_service.get_wallet().get_administrated_organizations()),
        )

    def is_super_admin(self) -> bool:
        """ Whether this user is superadmin

        Returns:
            is superadmin
        """
        return self.auth_service.is_super_admin()

    def has_required_tokens(self, context: OrganizationContract) -> bool:
        """ Whether user has any whitelisted tokens

        Args:
            context - context in which to check

        Returns:
            whether user has any whitelisted tokens
        """

        # whitelist not enforced
        if not context.token_id_whitelist:
            return True

        return self.get_required_tokens_balances(context).exists()

    def get_required_tokens_balances(self, context: OrganizationContract):
        """ Query returning all balances which have contracts whitelisted in context

            Args:
                context - context in which to get balances

            Returns:
                whitelisted balances
        """
        return Balance.select(Balance.balance, Balance.token_id, Balance.address, Balance.contract).where(
            Balance.address == self.auth_service.get_wallet().address,
            Balance.contract == context.contract,
            Balance.token_id.in_(context.token_id_whitelist),
            Balance.balance > 0
        )


def user_service_dependency(auth_service=AuthService):
    return UserServiceType(auth_service)


UserService = Depends(user_service_dependency)
