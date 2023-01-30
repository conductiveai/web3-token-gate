from collections import defaultdict
from typing import List

from fastapi import APIRouter

from dependencies.organization import GetContext
from exceptions.exceptions import ApiError
from models.organization import OrganizationContract
from schemas.common import ResponseSchema
from schemas.profile import Profile
from schemas.user import User, CreateProfile, UserContext, TokenBalance
from services.user import UserService, UserServiceType

router = APIRouter()


@router.get("/me", response_model=ResponseSchema[User])
def get_me(user_service: UserServiceType = UserService):
    """ Get Me """
    return ResponseSchema(
        error=False,
        data=user_service.get_me()
    )


@router.get("/balances", response_model=ResponseSchema[List[TokenBalance]])
def get_balances(user_service: UserServiceType = UserService, context: OrganizationContract = GetContext(required=True)):
    """ Get balances of whitelisted token IDs.

        If context has 10 ERC-1155 token IDs whitelisted, and a user owns 5 of those,
        this endpoint will return how many of each of 5 user owns.
    """
    return ResponseSchema(
        error=False,
        data=list(user_service.get_required_tokens_balances(context))
    )


@router.get("/profile", response_model=ResponseSchema[UserContext])
def get_profile(user_service: UserServiceType = UserService, context: OrganizationContract = GetContext(required=True)):
    """ Get own profile if it exists """

    profile = user_service.get_profile(context)

    return ResponseSchema(
        error=False,
        data=UserContext(
            profile=profile,
            balance=user_service.get_balance(context),
            relevant_balance=user_service.get_balance(context, only_relevant=True),
        )
    )


@router.post("/profile/create", response_model=ResponseSchema[Profile])
def create_profile(data: CreateProfile, user_service: UserServiceType = UserService, context=GetContext(required=True)):
    """ Create a new profile """

    if user_service.get_profile(context) is not None:
        raise ApiError("You already have a profile")

    balance = user_service.get_balance(context)

    if balance < context.threshold:
        raise ApiError('Insufficient balance')

    if not user_service.has_required_tokens(context):
        raise ApiError('Insufficient tokens')

    present_balances = user_service.get_required_tokens_balances(context)

    required_balances = defaultdict(lambda: 0)

    # count how many of each token id user tries to claim, also validate sizes
    for size in data.sizes:
        for size_name in size.sizes:
            if size_name not in ["S", "M", "L", "XL"]:
                raise ApiError("Invalid size")

        # += in case there are duplicate token ids
        required_balances[size.token_id] += len(size.sizes)

    for token_id, count in required_balances.items():
        for present_balance in present_balances:
            if present_balance.token_id == token_id:
                if present_balance.balance < count:
                    raise ApiError("You don't have this much tokens")
                else:
                    # found required token in needed quantity
                    break
        else:
            # token id was not found in wallet balances
            raise ApiError(f"You don't have token with id {token_id}")

    profile = user_service.create_profile(context=context, **data.dict())
    return ResponseSchema(
        error=False,
        data=profile,
        message=(
            "Successfully created profile"
        )
    )


@router.post("/profile/update", response_model=ResponseSchema[Profile])
def update_profile(data: CreateProfile, context=GetContext(required=True), user_service: UserServiceType = UserService):
    """ Update existing profile """

    if user_service.get_profile(context) is None:
        raise ApiError("You don't have a profile")

    profile = user_service.update_profile(context, **data.dict())

    return ResponseSchema(
        error=False,
        data=profile,
        message=(
            "Successfully updated profile"
        )
    )
