from adapters.blockscan import Blockscan
from models.chain import Chain


class TestBlockscan:

    def test_get_transactions(self, requests_mock, contract_1):

        with requests_mock("blockscan/transactions"):
            transactions = Blockscan.get_transactions(contract_1)

            assert len(list(transactions)) == 3

    def test_get_info(self, requests_mock):

        with requests_mock("blockscan/tokeninfo"):
            info = Blockscan.get_info("0xdAC17F958D2ee523a2206206994597C13D831ec7", Chain.get_by_id(1))
            assert info.name == "Tether USD"
