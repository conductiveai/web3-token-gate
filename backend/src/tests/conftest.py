import asyncio
import datetime
import inspect
import itertools
import json
import os
from collections import namedtuple
from contextlib import contextmanager, suppress
from typing import Any, Callable, Dict, List, Set, Union
from unittest.mock import patch
from urllib.parse import urlparse
import pytest
import pytz
import requests
from freezegun import freeze_time
from requests import Response

from dependencies.user import AuthServiceType
from models.contract import Contract
from models.organization import Organization, OrganizationContract
from models.wallet import Wallet
from services.user import UserServiceType
from services.verification import VerificationService
from settings import settings

if os.environ.get("ENV") != "TEST":
    raise ValueError("ENV must be set to TEST in order to run tests.")

if settings.database_host != "token_gating_db" and os.environ.get("I_DONT_WANT_TO_RUN_TESTS_IN_DOCKER") is None:
    raise ValueError(
        f"It looks like you are trying to run tests outside docker. Keep in mind that database specified "
        f"in your environment ({settings.database_host}) will be wiped out. If you are sure, please set "
        f"I_DONT_WANT_TO_RUN_TESTS_IN_DOCKER env variable"
    )


def pytest_configure():
    """
    This function is running before testing starts
    """


@pytest.fixture(scope="session", autouse=True)
def database():
    from database import db

    # drop all tables
    for table in db.execute_sql("select table_name from information_schema.tables where table_schema='public'"):
        db.execute_sql(f"DROP TABLE {table[0]} CASCADE")

    os.system("pem migrate")

    # execute init.sql (materialized view)
    with open("init.sql", "r") as f:
        db.execute_sql(f.read())

    # initialize database
    from models.chain import Chain

    for chain_id, name in settings.chains.items():
        Chain.get_or_create(
            id=chain_id,
            defaults={
                'name': name
            }
        )

    return db


@pytest.fixture(scope="function", autouse=True)
def preserve_db(database):
    """Preserves database state after each test"""

    with database.atomic() as tx:
        yield
        tx.rollback()


@pytest.fixture(scope="function")
def mock_settings():

    @contextmanager
    def context(**kwargs):
        old = {}
        for k, v in kwargs.items():
            old[k] = getattr(settings, k)
            setattr(settings, k, v)
        yield
        for k, v in old.items():
            setattr(settings, k, v)

    return context


@pytest.fixture
def requests_mock() -> Callable:
    """
    Mocks 'requests.api.request' method to return data from fixtures

    Returns:
        Function that accepts list of fixture names and returns a context manager, that mocks 'httpx.request' method
    """

    @contextmanager
    def _requests(*fixture_names: str):
        """
        Mocks httpx AsyncClient with fixtures.
        """

        class Mock:
            fixtures: List[Dict[str, Any]] = list(
                itertools.chain.from_iterable(
                    [
                        load_json_fixture(fixture_name + ".json")
                        for fixture_name in fixture_names
                    ]
                )
            )

            @classmethod
            def all_called(cls):
                return len(cls.fixtures) == 0

        def _clear_params(_request: Dict[str, Any], param: str):
            if _request.get("params"):
                _request["params"][param] = "**REDACTED**"
            return _request

        def _clear_headers(_request: Dict[str, Any], header: str):
            if _request.get("headers"):
                _request["headers"][header] = "**REDACTED**"
            return _request

        sanitizers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
            "api.etherscan.io": lambda _request: _clear_params(_request, "apikey"),
        }

        def request(
            method: str,
            url: str,
            **kwargs: Any,
        ):
            kwargs["url"] = url
            kwargs["method"] = method

            domain: str = urlparse(url).netloc

            if domain in sanitizers:
                kwargs = sanitizers[domain](kwargs)

            # encode params
            encoded_params: Set[str] = set()

            key: str
            value: Any

            params: Dict[str, str] = kwargs.get("params", None) or {}

            for key, value in params.items():
                if isinstance(value, (list, tuple)):
                    for v in value:
                        encoded_params.add(f"{key}={v}")
                else:
                    encoded_params.add(f"{key}={value}")

            for fixture in Mock.fixtures:
                if fixture["request"]["method"].lower() != kwargs["method"].lower():
                    continue

                if fixture["request"].get("url") != kwargs["url"]:
                    continue

                if set(fixture["request"].get("params") or []) != encoded_params:
                    continue

                if fixture["request"].get("headers") != kwargs.get("headers"):
                    continue

                if fixture["request"].get("data") != kwargs.get("data"):
                    continue

                Mock.fixtures.remove(fixture)
                r = Response()
                r.status_code = fixture["response"]["status"]
                r._content = json.dumps(fixture["response"]["body"]).encode()
                r.headers = fixture["response"].get("headers", {})
                return r

            raise ValueError(
                f"No matching response found for request\n\n"
                f"method:  {kwargs['method']}\n"
                f"url:     {kwargs['url']}\n"
                f"params:  {encoded_params}\n"
                f"headers: {kwargs.get('headers')}"
            )

        with patch.object(requests.api, "request", request):
            yield Mock

        assert Mock.all_called(), "Not all fixtures were called"

    return _requests


def load_text_fixture(file_name: str) -> str:
    """Loads data from fixture folder as str"""

    current_path = os.path.dirname(os.path.abspath(__file__))

    path = os.path.join(f"{current_path}/fixtures", file_name)

    with open(path, "r") as f:
        return f.read()


def load_json_fixture(file_name: str) -> Union[Dict, List]:
    """Loads data from fixture folder and transforms it into JSON"""

    text = load_text_fixture(file_name)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Fixture {file_name} is not valid JSON") from e


@pytest.fixture(scope="function")
def organization_1():
    return Organization.create(
        name="Organization 1",
        status=Organization.Status.ACTIVE,
    )


@pytest.fixture(scope="function")
def contract_1():
    """ ERC 20 contract - 0x0000000000000000000000000000000000000100 """
    return Contract.create(
        token_name="Contract 1",
        address="0x0000000000000000000000000000000000000100",
        erc_standard=20,
        holders=0,
        chain=1,
        decimals=18
    )


@pytest.fixture(scope="function")
def contract_2():
    return Contract.create(
        token_name="Contract 1",
        address="0x0000000000000000000000000000000000000100",
        erc_standard=1155,
        holders=0,
        chain=1,
        decimals=0
    )


@pytest.fixture(scope="function")
def context_1(contract_1, organization_1):
    return OrganizationContract.create(
        contract=contract_1,
        organization=organization_1,
    )


@pytest.fixture(scope="function")
def user_service():
    """ User service for wallet 0x0000000000000000000000000000000000000010 """
    Wallet.create(
        address="0x0000000000000000000000000000000000000010",
        chain=1
    )
    with freeze_time(datetime.datetime.fromtimestamp(0, tz=pytz.UTC)):
        service = UserServiceType(
            AuthServiceType(
                token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3YWxsZXRfYWRkcmVzcyI6IjB4MDAwMDAwMDAwMDAwMDAwMDAwMD"
                      "AwMDAwMDAwMDAwMDAwMDAwMDAxMCIsImV4cCI6ODY0MDB9.iVri43uk6swmkNwSP_mrEvrCKDlCxmkVefJjKdH5suo"
            )
        )
        yield service


@pytest.fixture(scope="function")
def context_2(contract_2, organization_1):
    """ Context with 1155 token, whitelisted IDs: 1, 2, 3"""
    return OrganizationContract.create(
        contract=contract_2,
        organization=organization_1,
        token_id_whitelist=[1, 2, 3]
    )


@pytest.fixture(scope="function")
def superadmin():
    return Wallet.create(
        address="0x0000000000000000000000000000000000000099",
        chain=1,
        is_super_admin=True
    )


def user_service_of(wallet):
    jwt = VerificationService.create_jwt(wallet_address=wallet.address)
    return UserServiceType(
        AuthServiceType(
            token=jwt
        )
    )
