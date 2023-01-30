import re

from peewee import CharField, Model

address_regex = re.compile("^0x[a-fA-F0-9]{40}$")
hash_regex = re.compile("^0x[a-fA-F0-9]{64}$")


class Web3AddressField(CharField):
    """ Field that stores a Web3 address (0x prefixed lowercase 20 byte hex string) """

    def __init__(self, **kwargs):
        if 'max_length' in kwargs:
            del kwargs['max_length']

        super().__init__(max_length=42, **kwargs)

    def db_value(self, value):
        if not isinstance(value, str):
            raise ValueError("Web3AddressField must be a string")

        if not address_regex.match(value):
            raise ValueError(f"{value} is not a valid Ethereum address")

        return super().db_value(value.lower())

    def python_value(self, value):
        return value.lower()


class Web3HashField(CharField):
    """ Field that stores a Web3 hash (0x prefixed lowercase 32 byte hex string) """

    def __init__(self, **kwargs):
        if 'max_length' in kwargs:
            del kwargs['max_length']

        super().__init__(max_length=66, **kwargs)

    def db_value(self, value):
        if not isinstance(value, str):
            raise ValueError("Web3HashField must be a string")

        if not hash_regex.match(value):
            raise ValueError(f"{value} is not a valid Ethereum hash")

        return super().db_value(value.lower())

    def python_value(self, value):
        return value.lower()
