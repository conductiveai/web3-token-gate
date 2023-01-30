from typing import Optional

from pydantic import BaseModel, Field

from schemas.common import Web3Address, Web3Hash


class BlockScanTransaction(BaseModel):
    block_number: int = Field(alias="blockNumber")
    timestamp: int = Field(alias="timeStamp")
    hash: Web3Hash
    nonce: int
    block_hash: Web3Hash = Field(alias="blockHash")
    transaction_index: int = Field(alias="transactionIndex")
    index: int = Field(alias="transactionIndex")
    from_address: Web3Address = Field(alias="from")
    to_address: Web3Address = Field(alias="to")
    value: Optional[int]
    token_value: Optional[int] = Field(alias="tokenValue")
    gas: int
    gas_price: int = Field(alias="gasPrice")
    gas_used: int = Field(alias="gasUsed")
    cumulative_gas_used: int = Field(alias="cumulativeGasUsed")
    input: str
    token_id: Optional[int] = Field(alias="tokenID")
    confirmations: int

    def get_value(self):
        return self.token_value or self.value


class TokenInfo(BaseModel):
    contract_address: Web3Address = Field(alias="contractAddress")
    name: str = Field(alias="tokenName")
    symbol: str
    divisor: int
    standard: str = Field(alias="tokenType")
    total_supply: int = Field(alias="totalSupply")
    blue_check: bool = Field(alias="blueCheckmark")
    description: str
    price_usd: Optional[float] = Field(alias="priceUSD")

    def get_erc_standard(self) -> Optional[int]:
        standard = self.standard.lower()
        standard = standard.replace("erc", "")
        if not standard:
            return None

        return int(standard)
