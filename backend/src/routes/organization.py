import csv
import io
from collections import defaultdict
from typing import List

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from dependencies.organization import GetOrganization, RequireContext, RequireOrganization
from exceptions.exceptions import ApiError
from models.chain import Chain
from models.contract import Contract
from models.organization import Organization, OrganizationContract
from models.wallet import Wallet
from schemas.common import ResponseSchema, Web3Address
from schemas.contract import Contract as ContractSchema
from schemas.organization import Breakdown, CreateContractRequest, AddAdminRequest, \
    RemoveAdminRequest, UpdateContextRequest
from schemas.profile import Profile
from schemas.organization import Organization as OrgSchema
from services.user import UserServiceType, UserService

router = APIRouter(dependencies=[UserService])


@router.get("/contracts", response_model=ResponseSchema[List[ContractSchema]])
def get_contracts(
        organization: Organization = RequireOrganization
):
    """ Get all contracts within given organization """

    return ResponseSchema(
        error=False,
        data=list(organization.contracts)
    )


@router.get("/holders", response_model=ResponseSchema[List[Profile]])
def get_holders(
        context: OrganizationContract = RequireContext,
):
    """ Get profiles associated with given context """

    return ResponseSchema(
        error=False,
        data=list(context.get_profiles())
    )


@router.get("/tx/breakdowns", response_model=ResponseSchema[List[Breakdown]])
def get_transaction_breakdowns(
        organization: Organization = RequireOrganization
):
    """ Get transaction breakdowns by contract within given organization """

    return ResponseSchema(
        error=False,
        data=organization.get_tx_breakdowns()
    )


@router.get("/wallet/breakdowns", response_model=ResponseSchema[List[Breakdown]])
def get_wallet_breakdowns(
        organization: Organization = RequireOrganization
):
    """ Get profile breakdowns by contract within given organization """
    return ResponseSchema(
        error=False,
        data=organization.get_wallet_breakdowns()
    )


@router.get("/stats")
def get_stats(organization: Organization = RequireOrganization):
    """ Get organization stats across all contracts """

    return ResponseSchema(
        error=False,
        data={
            "transactions_24h": organization.count_transactions(1),
            "transactions_7d": organization.count_transactions(7),
            "transactions_30d": organization.count_transactions(30),
            "users_24h": organization.count_users(1),
            "users_7d": organization.count_users(7),
            "users_30d": organization.count_users(30),
        }
    )


@router.get("/export")
def export(context: OrganizationContract = RequireContext):
    """ Export context profiles as CSV """

    file = io.StringIO()
    csv_writer = csv.writer(file)
    csv_writer.writerow([
        'first_name', 'last_name', 'email',
        'phone', 'country', 'city', 'region',
        'postal_code', 'address1', 'address2',
        'address3', 'token_id', 'size', 'count'
    ])

    for profile in context.get_profiles():
        profile_cols = [
            profile.first_name, profile.last_name, profile.email, profile.phone,
            profile.country, profile.city, profile.region, profile.postal_code,
            profile.address1, profile.address2, profile.address3
        ]

        if profile.sizes:

            # stack same size for same token together
            for token_sizes in profile.sizes:
                token_id = token_sizes['token_id']
                sizes = token_sizes['sizes']
                sizes_with_count = defaultdict(lambda: 0)

                for size in sizes:
                    sizes_with_count[size] += 1

                # write row for each unique token + size, duplicating common profile data
                for size, count in sizes_with_count.items():
                    csv_writer.writerow([*profile_cols, token_id, size, count])
        else:
            csv_writer.writerow([*profile_cols, None, None, None])

    file.seek(0)

    filename = f"{context.organization.name}-{context.contract.token_name}.csv"

    return StreamingResponse(
        file,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.post("/contract/create", response_model=ResponseSchema[ContractSchema])
def create_contract(
        data: CreateContractRequest,
        organization: Organization = RequireOrganization
):
    """ Create new context within organization """

    contract = Contract.get_or_init(
        address=data.address,
        chain=data.chain,
    )

    org_contract = organization.add_contract(
        contract,
        threshold=data.threshold or 1,
        token_id_whitelist=data.token_id_whitelist,
        title=data.title,
        image=data.image,
        texts={
            'greeting': '👋 Hey anon. Prove you\'re a holder, connect you wallet',
            'accepted':  '👈 Great anon, you have {balance} token(s). Complete the form.',
            'not_accepted': 'You need {threshold} token(s) to participate.',
            'completed': '👍 Great anon, you have completed your profile.'
        }
    )

    return ResponseSchema(
        error=False,
        data=org_contract
    )


@router.post("/contract/delete", response_model=ResponseSchema[ContractSchema])
def delete_contract(
        context: OrganizationContract = RequireContext
):
    """ Deactivate context """

    context.deactivate()

    return ResponseSchema(
        error=False,
        data=context.contract
    )


@router.post("/admin/add", response_model=ResponseSchema[Web3Address])
def add_admin(
        data: AddAdminRequest,
        organization: Organization = RequireOrganization
):
    """ Add admin to given organization """

    wallet, _ = Wallet.get_or_create(
        address=data.address,
        defaults={
            'chain': Chain.get(id=1)
        }
    )

    organization.add_admin(wallet)

    return ResponseSchema(
        error=False,
        data=data.address,
        message="Admin added successfully"
    )


@router.post("/admin/remove", response_model=ResponseSchema[Web3Address])
def remove_admin(
        data: RemoveAdminRequest,
        organization: Organization = RequireOrganization
):
    """ Remove admin from given organization """

    wallet = Wallet.get_or_none(
        address=data.address,
    )

    if not wallet:
        raise ApiError('Wallet does not exist')

    organization.remove_admin(wallet)

    return ResponseSchema(
        error=False,
        data=data.address,
        message="Admin removed successfully"
    )


@router.get("/", response_model=ResponseSchema[OrgSchema])
def get_org(organization: Organization = RequireOrganization):
    """ Get organization data """

    return ResponseSchema(
        error=False,
        data=organization
    )


@router.post("/context/update")
def update_context(
        data: UpdateContextRequest,
        context: OrganizationContract = RequireContext
):
    """ Update context """

    # filter out empty values
    data.texts = {k: v for k, v in data.texts.items() if v}

    context.update_context(**data.dict())

    return ResponseSchema(
        error=False,
        message="Context updated successfully"
    )
