from evmdasm import EvmBytecode
from enum import Enum, auto
from typing import Optional, Dict
from web3 import Web3
import requests


# ERC interfaces that derive the 4byte keccak hash from the smart contract code
class ContractInterfaces(Enum):
    ERC_20 = [
        'balanceOf(address)',
        'totalSupply()',
        'transfer(address,uint256)',
        'transferFrom(address,address,uint256)',
        'approve(address,uint256)',
        'allowance(address,address)'
    ]

    ERC_721 = [
        'balanceOf(address)',
        'ownerOf(uint256)',
        'approve(address,uint256)',
        'getApproved(uint256)',
        'setApprovalForAll(address,bool)',
        'isApprovedForAll(address,address)',
        'transferFrom(address,address,uint256)',
        'safeTransferFrom(address,address,uint256)',
        'safeTransferFrom(address,address,uint256,bytes)'
    ]

    ERC_1155 = [
        'setApprovalForAll(address,bool)',
        'isApprovedForAll(address,address)',
        'safeTransferFrom(address,address,uint256,uint256,bytes)',
        'safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)'
    ]

    PROXY_CONTRACT = [
        'implementation()',
        'upgradeTo(address)',
        'upgradeToAndCall(address,bytes)'
    ]


class AddressType(Enum):
    UNKNOWN = auto()
    EOA = auto()
    CONTRACT = auto()
    ERC_20_CONTRACT = auto()
    ERC_721_CONTRACT = auto()
    ERC_1155_CONTRACT = auto()


class ContractDetector:
    """ Allows to detect contract type only based on contract address and chain """

    def __init__(self, rpc_map: Dict[int, str]):
        """ Initialize contract detector.

            Args:
                rpc_map - maps chain id to RPC url
        """

        self.rpc_map = rpc_map

    def get_address_code(self, address: str, chain: int):
        """
        Fetch the raw contract bytecode

        :param address: Ethereum address
        :param chain: Canonical chain id
        """

        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "params": [
                address,
                "latest"
            ],
            "method": "eth_getCode"
        }

        rpc = self.rpc_map.get(chain)

        if not rpc:
            raise ValueError(f"No RPC provided for chain {chain}")

        r = requests.post(rpc, json=payload)
        data = r.json()
        return data['result'] if 'result' in data and data['result'] and data['result'] != '0x' else None

    @classmethod
    def get_function_signatures(cls, code: str):
        """
        Extract function signatures from the raw bytecode

        :param code: Raw contract bytecode retrieved by eth_getCode call to RPC node
        """

        # Unique set of function signatures
        signatures = set()

        # Extract the opcodes from the bytecode using evmdasm
        for instruction in EvmBytecode(code).disassemble():

            # Extract the function signature from the PUSH4 opcode
            if instruction.name == 'PUSH4':
                # The operand contains the signature
                signatures.add(instruction.operand)

        data = []
        for signature in signatures:
            r = requests.get(f'https://raw.githubusercontent.com/ethereum-lists/4bytes/master/signatures/{signature}')
            data.extend(r.text.splitlines())

        if not data:
            return None

        # Let's return the set of function signatures
        return data

    def get_proxy_address(
        self,
        code: Optional[str] = None,
        signatures: Optional[str] = None,
        address: Optional[str] = None,
        chain: int = None,
    ):
        """
        Detect if the contract address is a proxy contract

        :param code: Raw contract bytecode retrieved by eth_getCode call to RPC node
        :param signatures: Set of function signatures retrieved by get_function_signatures
        :param address: Ethereum address
        :param chain: Canonical chain id
        """

        # --------------
        # EIP-1167 Proxy
        # --------------
        # reference: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/Clones.sol
        if code and code.lower().startswith('0x3d602d80600a3d3981f3363d3d373d3d3d363d73'):
            return code[42:82]

        # --------------
        # ERC-1967 Proxy
        # --------------
        # reference: https://ethereum.stackexchange.com/questions/70515/usd-coin-balance-check-by-web3
        # example: USDC uses the upgradable proxy contract here:
        # https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48#readContract
        if signatures and 'implementation()' in signatures:

            rpc = self.rpc_map.get(chain)

            if not rpc:
                raise ValueError(f"RPC not provided for chain {chain}")

            w3 = Web3(Web3.HTTPProvider(rpc))
            contract_address = w3.eth.get_storage_at(address, '0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3')
            return f'0x{contract_address.hex()[26:]}'

        return None

    def get_address_type(self, address: str, chain: int):
        """
        Return Enum of the address type

        :param address: Ethereum address
        :param chain: Canonical chain id
        """

        address = Web3.toChecksumAddress(address)

        # -------------------------------
        # Get the address bytecode if any
        # -------------------------------
        code = self.get_address_code(address, chain)

        # If there is no bytecode, then it's an EOA (normal wallet address)
        if not code:
            return AddressType.EOA

        # -----------------------------
        # Get matching 4byte signatures
        # -----------------------------
        signatures = self.get_function_signatures(code)

        # ------------------------------
        # Check if it's a proxy contract
        # ------------------------------
        proxy_address = self.get_proxy_address(code=code, signatures=signatures, address=address)

        # If it is a proxy contract, then we need to get the implementation address
        if proxy_address:
            return self.get_address_type(proxy_address, chain)

        # If no signatures were detected, at a minimum this is a contract
        if not signatures:
            return AddressType.CONTRACT

        # -----------------------------------------------
        # Use CONTRACT_INTERFACES to check subset matches
        # -----------------------------------------------
        if set(ContractInterfaces.ERC_20.value).issubset(signatures):
            return AddressType.ERC_20_CONTRACT

        if set(ContractInterfaces.ERC_721.value).issubset(signatures):
            return AddressType.ERC_721_CONTRACT

        if set(ContractInterfaces.ERC_1155.value).issubset(signatures):
            return AddressType.ERC_1155_CONTRACT

        return AddressType.CONTRACT
