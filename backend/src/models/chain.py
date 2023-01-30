from peewee import IntegerField, CharField

from database import BaseModel


class Chain(BaseModel):
    """ A blockchain network """

    id = IntegerField(primary_key=True)
    name = CharField(max_length=128)
