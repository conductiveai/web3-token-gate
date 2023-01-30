import time

from fastapi import APIRouter

from dependencies.organization import GetContext
from schemas.common import ResponseSchema
from schemas.organization import ContextWithOrg

router = APIRouter()


@router.get("/{context_uuid}", response_model=ResponseSchema[ContextWithOrg])
def get_context(context=GetContext(required=True)):
    """ Get context by UUID """
    return ResponseSchema(
        error=False,
        data=context
    )
