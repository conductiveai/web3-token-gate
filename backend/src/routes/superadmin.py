from typing import List

from fastapi import APIRouter

from dependencies.organization import GetOrganization
from dependencies.superadmin import GetSuperAdmin
from models.chain import Chain
from models.contract import Contract
from models.organization import Organization
from models.wallet import Wallet
from schemas.common import ResponseSchema
from schemas.superadmin import CreateOrganizationRequest
from schemas.organization import Organization as OrgSchema

# all endpoints attached to this router requre superadmin permissions
router = APIRouter(dependencies=[GetSuperAdmin])


@router.post("/organization/create", response_model=ResponseSchema[OrgSchema])
def create_organization(data: CreateOrganizationRequest):
    """ Create a new organization """

    org: Organization = Organization.create(
        name=data.name
    )

    chain = Chain.get_or_create(
        id=1,
        defaults={
            'name': 'Ethereum'
        }
    )

    for admin in data.admins:
        wallet, _ = Wallet.get_or_create(
            address=admin,
            defaults={
                'chain': chain
            }
        )
        org.add_admin(wallet)

    contract: Contract

    for contract in data.contracts:
        org.add_contract(contract)

    return ResponseSchema(
        error=False,
        data=org,
        message='Organization created successfully'
    )


@router.post("/organization/{org_id}/disable", response_model=ResponseSchema[OrgSchema])
def delete_organization(org: Organization = GetOrganization(required=True)):
    """ Delete given organization """

    org.status = Organization.Status.DELETED
    org.save()

    return ResponseSchema(
        error=False,
        data=org,
        message='Organization deleted successfully'
    )


@router.get("/organization/list", response_model=ResponseSchema[List[OrgSchema]])
def list_organizations():
    """ List all active organizations """

    return ResponseSchema(
        error=False,
        data=list(Organization.select().where(Organization.status == Organization.Status.ACTIVE))
    )


@router.get("/organization/{org_id}", response_model=ResponseSchema[OrgSchema])
def get_organization(org: Organization = GetOrganization(required=True)):
    """ Get organization by id """

    return ResponseSchema(
        error=False,
        data=org
    )

