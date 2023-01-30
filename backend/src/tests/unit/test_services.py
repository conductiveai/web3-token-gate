import datetime
from unittest.mock import patch

import pytest
import pytz
from freezegun import freeze_time

from adapters.blockscan import Blockscan
from database import db
from exceptions.exceptions import ApiError
from models.balance import Balance
from models.contract import Contract
from models.profile import Profile
from models.transaction import Transaction
from models.wallet import Wallet
from schemas.blockscan import BlockScanTransaction
from services.verification import VerificationService
from tests.conftest import user_service_of


class TestVerification:

    def test_generate_message(self):
        message = VerificationService.get_message("0x0d846e45dbf44203cbc540dca4b9c2f646c52cd1", 1674728600)
        assert message == "Please sign this message to verify your address: " \
                          "3438041c16b80630e2caca34975b150d627ce0596ae87252cfb26cffa94db8af.1674728600"

    def test_verify_message(self):
        time = datetime.datetime.fromtimestamp(1674728300, tz=pytz.UTC)

        with freeze_time(time):
            is_verified = VerificationService.verify(
                wallet_address="0x0d846e45dbf44203cbc540dca4b9c2f646c52cd1",

                signature="0x7222f70f3778efe4e3b47fde37fc0c89a08bee60e870cda5a50aa94e31052a88"
                          "0ead5e189ac665688b62e0074115fe165f54795e78c074514af848ee623ffce11b",

                message="Please sign this message to verify your address: "
                        "3438041c16b80630e2caca34975b150d627ce0596ae87252cfb26cffa94db8af.1674728600"
            )
            assert is_verified is not None

            assert Wallet.select().where(
                Wallet.address == "0x0d846e45dbf44203cbc540dca4b9c2f646c52cd1",
                Wallet.verified_at == time,
            ).exists()

            with pytest.raises(ApiError):
                VerificationService.verify(
                    wallet_address="0x0d846e45dbf44203cbc540dca4b9c2f646c52cd2",  # <- 2 at the end

                    signature="0x7222f70f3778efe4e3b47fde37fc0c89a08bee60e870cda5a50aa94e31052a88"
                              "0ead5e189ac665688b62e0074115fe165f54795e78c074514af848ee623ffce11b",

                    message="Please sign this message to verify your address: "
                            "3438041c16b80630e2caca34975b150d627ce0596ae87252cfb26cffa94db8af.1674728600"
                )

            assert not Wallet.select().where(Wallet.address == "0x0d846e45dbf44203cbc540dca4b9c2f646c52cd2").exists()

    def test_create_jwt(self):
        with freeze_time(datetime.datetime.fromtimestamp(0, tz=pytz.utc)):
            jwt = VerificationService.create_jwt("0x0000000000000000000000000000000000000000")
            assert jwt == (
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3YWxsZXRfYWRkcmVzcyI6IjB4MDAwMDAwMDAwMDAwMDAwMDAwMD"
                "AwMDAwMDAwMDAwMDAwMDAwMDAwMCIsImV4cCI6ODY0MDB9.7durNx1NNRR_mC8gG6u2Ty8p0Y0rFB7LGXn0cCQAR9Y"
            )


class TestContractService:

    def test_process_erc20_contract(self):

        contract_20 = Contract.create(
            address="0x0000000000000000000000000000000000000000",
            token_name="TEST",
            erc_standard=20,
            holders=0,
            chain=1,
            decimals=18
        )

        return_value = [
            BlockScanTransaction.construct(
                block_number=0,
                timestamp=0,
                hash="0x0000000000000000000000000000000000000000000000000000000000000000",
                nonce=0,
                block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
                transaction_index=0,
                index=0,
                from_address="0x0000000000000000000000000000000000000001",
                to_address="0x0000000000000000000000000000000000000002",
                value=1,
                token_value=0,
                gas=0,
                gas_price=0,
                gas_used=0,
                cumulative_gas_used=0,
                input="",
                token_id=None,
                confirmations=0
            ),
            BlockScanTransaction.construct(
                block_number=0,
                timestamp=0,
                hash="0x0000000000000000000000000000000000000000000000000000000000000001",
                nonce=0,
                block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
                transaction_index=0,
                index=0,
                from_address="0x0000000000000000000000000000000000000002",
                to_address="0x0000000000000000000000000000000000000003",
                value=1,
                token_value=0,
                gas=0,
                gas_price=0,
                gas_used=0,
                cumulative_gas_used=0,
                input="",
                token_id=None,
                confirmations=0
            )
        ]

        with patch.object(Blockscan, 'get_transactions') as p:
            p.return_value = return_value
            from services.contract import process_contract
            process_contract(contract_20)

        db.execute_sql('refresh materialized view concurrently "public"."wallet_balances";')

        assert Balance.select().where(
            Balance.contract == contract_20,
            Balance.address == "0x0000000000000000000000000000000000000001",
            Balance.balance == -1
        ).exists()

        assert Balance.select().where(
            Balance.contract == contract_20,
            Balance.address == "0x0000000000000000000000000000000000000002",
            Balance.balance == 0
        ).exists()

        assert Balance.select().where(
            Balance.contract == contract_20,
            Balance.address == "0x0000000000000000000000000000000000000003",
            Balance.balance == 1
        ).exists()

    def test_process_erc1155_contract(self):

        contract_1155 = Contract.create(
            address="0x0000000000000000000000000000000000000000",
            token_name="TEST",
            erc_standard=1155,
            holders=0,
            chain=1,
            decimals=0
        )

        return_value = [
            BlockScanTransaction.construct(
                block_number=0,
                timestamp=0,
                hash="0x0000000000000000000000000000000000000000000000000000000000000000",
                nonce=0,
                block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
                transaction_index=0,
                index=0,
                from_address="0x0000000000000000000000000000000000000001",
                to_address="0x0000000000000000000000000000000000000002",
                value=0,
                token_value=1,
                gas=0,
                gas_price=0,
                gas_used=0,
                cumulative_gas_used=0,
                input="",
                token_id=1,
                confirmations=0
            ),
            BlockScanTransaction.construct(
                block_number=0,
                timestamp=0,
                hash="0x0000000000000000000000000000000000000000000000000000000000000001",
                nonce=0,
                block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
                transaction_index=0,
                index=0,
                from_address="0x0000000000000000000000000000000000000002",
                to_address="0x0000000000000000000000000000000000000003",
                value=0,
                token_value=1,
                gas=0,
                gas_price=0,
                gas_used=0,
                cumulative_gas_used=0,
                input="",
                token_id=1,
                confirmations=0
            )
        ]

        with patch.object(Blockscan, 'get_transactions') as p:
            p.return_value = return_value
            from services.contract import process_contract
            process_contract(contract_1155)

        db.execute_sql('refresh materialized view concurrently "public"."wallet_balances";')

        assert Balance.select().where(
            Balance.contract == contract_1155,
            Balance.address == "0x0000000000000000000000000000000000000001",
            Balance.balance == -1,
            Balance.token_id == 1,
        ).exists()

        assert Balance.select().where(
            Balance.contract == contract_1155,
            Balance.address == "0x0000000000000000000000000000000000000002",
            Balance.balance == 0,
            Balance.token_id == 1,
        ).exists()

        assert Balance.select().where(
            Balance.contract == contract_1155,
            Balance.address == "0x0000000000000000000000000000000000000003",
            Balance.balance == 1,
            Balance.token_id == 1,
        ).exists()


class TestUserService:

    @freeze_time(datetime.datetime.fromtimestamp(0, tz=pytz.UTC))
    def test_create_profile(self, context_1, user_service):

        user_service.create_profile(
            context_1,
            first_name="Test",
            last_name="User",
            email="user@example.com",
            phone="+1234567890",
            country="US",
            address1="Example Street 1",
            address2="Example Street 2",
            address3="Example Street 3",
            city="Example City",
            region="Example Region",
            postal_code="12345",
        )

        assert Profile.select().where(
            Profile.context == context_1,
            Profile.wallet == user_service.auth_service.get_wallet(),
            Profile.first_name == "Test",
            Profile.last_name == "User",
            Profile.email == "user@example.com",
            Profile.phone == "+1234567890",
            Profile.country == "US",
            Profile.address1 == "Example Street 1",
            Profile.address2 == "Example Street 2",
            Profile.address3 == "Example Street 3",
            Profile.city == "Example City",
            Profile.region == "Example Region",
            Profile.postal_code == "12345",
        ).exists()

    @freeze_time(datetime.datetime.fromtimestamp(0, tz=pytz.UTC))
    def test_update_profile(self, context_1, user_service):

        Profile.create(
            context=context_1,
            wallet=user_service.auth_service.get_wallet(or_create=True),
            first_name="Test",
            last_name="User",
            email="user@example.com",
            phone="+1234567890",
            country="US",
            address1="Example Street 1",
            address2="Example Street 2",
            address3="Example Street 3",
            city="Example City",
            region="Example Region",
            postal_code="12345",
            created_at=datetime.datetime.fromtimestamp(0, tz=pytz.UTC),
            updated_at=datetime.datetime.fromtimestamp(0, tz=pytz.UTC),
        )

        user_service.update_profile(
            context_1,
            first_name="Test-",
            last_name="User-",
            email="user@example.com-",
            phone="+1234567890-",
            country="US-",
            address1="Example Street 1-",
            address2="Example Street 2-",
            address3="Example Street 3-",
            city="Example City-",
            region="Example Region-",
            postal_code="12345-",
        )

        assert Profile.select().where(
            Profile.context == context_1,
            Profile.wallet == user_service.auth_service.get_wallet(),
            Profile.first_name == "Test-",
            Profile.last_name == "User-",
            Profile.email == "user@example.com-",
            Profile.phone == "+1234567890-",
            Profile.country == "US-",
            Profile.address1 == "Example Street 1-",
            Profile.address2 == "Example Street 2-",
            Profile.address3 == "Example Street 3-",
            Profile.city == "Example City-",
            Profile.region == "Example Region-",
            Profile.postal_code == "12345-",
        ).exists()

    @freeze_time(datetime.datetime.fromtimestamp(0, tz=pytz.UTC))
    def test_get_profile(self, context_1, user_service):

        profile = Profile.create(
            context=context_1,
            wallet=user_service.auth_service.get_wallet(or_create=True),
            first_name="Test",
            last_name="User",
            email="[...]",
            phone="[...]",
            country="US",
            address1="[...]",
            address2="[...]",
            address3="[...]",
            city="[...]",
            region="[...]",
            postal_code="[...]",
            created_at=datetime.datetime.fromtimestamp(0, tz=pytz.UTC),
            updated_at=datetime.datetime.fromtimestamp(0, tz=pytz.UTC),
        )

        assert user_service.get_profile(context_1) == profile

    @freeze_time(datetime.datetime.fromtimestamp(0, tz=pytz.UTC))
    def test_get_balance(self, context_2, user_service):

        Transaction.create(
            contract=context_2.contract,
            from_address="0x0000000000000000000000000000000000000000",
            to_address=user_service.auth_service.get_wallet(or_create=True).address,
            block_number=1,
            value=5,
            gas=1,
            gas_price=1,
            gas_used=1,
            cumulative_gas_used=1,
            nonce=1,
            timestamp=datetime.datetime.fromtimestamp(0, tz=pytz.UTC),
            hash="0x0000000000000000000000000000000000000000000000000000000000000000",
            block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
            index=0,
            chain=1,
            confirmations=1,
            token_id=1
        )
        Transaction.create(
            contract=context_2.contract,
            from_address="0x0000000000000000000000000000000000000000",
            to_address=user_service.auth_service.get_wallet(or_create=True).address,
            block_number=1,
            value=1,
            gas=1,
            gas_price=1,
            gas_used=1,
            cumulative_gas_used=1,
            nonce=1,
            timestamp=datetime.datetime.fromtimestamp(0, tz=pytz.UTC),
            hash="0x0000000000000000000000000000000000000000000000000000000000000001",
            block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
            index=0,
            chain=1,
            confirmations=1,
            token_id=2
        )
        Transaction.create(
            contract=context_2.contract,
            from_address="0x0000000000000000000000000000000000000000",
            to_address=user_service.auth_service.get_wallet(or_create=True).address,
            block_number=1,
            value=5,
            gas=1,
            gas_price=1,
            gas_used=1,
            cumulative_gas_used=1,
            nonce=1,
            timestamp=datetime.datetime.fromtimestamp(0, tz=pytz.UTC),
            hash="0x0000000000000000000000000000000000000000000000000000000000000002",
            block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
            index=0,
            chain=1,
            confirmations=1,
            token_id=4
        )

        db.execute_sql('refresh materialized view concurrently "public"."wallet_balances";')

        assert user_service.get_balance(context_2, only_relevant=True) == 6
        assert user_service.get_balance(context_2) == 11

    def test_has_access(self, context_1, superadmin):

        admin = Wallet.create(
            address="0x0000000000000000000000000000000000000011",
            chain=1
        )

        user = Wallet.create(
            address="0x0000000000000000000000000000000000000012",
            chain=1
        )

        context_1.organization.add_admin(admin)

        assert user_service_of(admin).has_access(context_1)
        assert user_service_of(user).has_access(context_1) is False
        assert user_service_of(superadmin).has_access(context_1)

    @pytest.mark.parametrize(
        "transactions, expected",
        [        # from                                         to                                          value id
            ([
                 ["0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000010", 2, 1],
                 ["0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000010", 5, 5],
                 ["0x0000000000000000000000000000000000000010", "0x0000000000000000000000000000000000000000", 1, 1],
             ], True),
            ([
                 ["0x0000000000000000000000000000000000000001", "0x0000000000000000000000000000000000000010", 1, 1],
                 ["0x0000000000000000000000000000000000000001", "0x0000000000000000000000000000000000000010", 4, 4],
                 ["0x0000000000000000000000000000000000000010", "0x0000000000000000000000000000000000000001", 1, 1],
             ], False),
            ([
                 ["0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000010", 1, 4],
                 ["0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000010", 2, 5],
                 ["0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000010", 3, 6],
             ], False),
        ]
    )
    @freeze_time(datetime.datetime.fromtimestamp(0, tz=pytz.UTC))
    def test_has_required_tokens(self, context_2, user_service, transactions, expected):
        for from_, to, value, token_id in transactions:
            Transaction.create(
                contract=context_2.contract,
                from_address=from_,
                to_address=to,
                block_number=1,
                value=value,
                gas=1,
                gas_price=1,
                gas_used=1,
                cumulative_gas_used=1,
                nonce=1,
                timestamp=datetime.datetime.fromtimestamp(0, tz=pytz.UTC),
                hash="0x0000000000000000000000000000000000000000000000000000000000000000",
                block_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
                index=0,
                chain=1,
                confirmations=1,
                token_id=token_id
            )

        db.execute_sql('refresh materialized view concurrently "public"."wallet_balances";')

        assert user_service.has_required_tokens(context_2) is expected
