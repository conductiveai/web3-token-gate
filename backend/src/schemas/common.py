from typing import Type, TypeVar, Generic, Optional

from pydantic import constr
from pydantic.generics import GenericModel


Web3Address: Type[str] = constr(
    regex=r"^0x[a-f\d]{40}$", strip_whitespace=True, to_lower=True
)

Web3Hash: Type[str] = constr(
    regex=r"^0x[a-f\d]{64}$", strip_whitespace=True, to_lower=True
)

T = TypeVar("T")


class ResponseSchema(GenericModel, Generic[T]):
    error: bool
    message: Optional[str]
    data: Optional[T]


class ChainField(int):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: int):
        from models.chain import Chain

        chain = Chain.get_or_none(id=v)
        if not chain:
            raise ValueError(f'Chain {v} does not exist')

        return chain
