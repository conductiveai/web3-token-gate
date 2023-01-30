import logging
from typing import List, Dict

from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):

    version = "0.0.0"
    title = "Conductive web3 Token Gate"

    log_level = Field(logging.INFO, env="LOG_LEVEL")
    log_format = Field("[%(asctime)s][%(levelname)s] %(message)s", env="LOG_FORMAT")
    debug = Field(False, env="DEBUG")

    database_name: str = Field(..., env="DATABASE_NAME")
    database_user: str = Field(..., env="DATABASE_USER")
    database_password: SecretStr = Field(..., env="DATABASE_PASSWORD")
    database_host: str = Field(..., env="DATABASE_HOST")
    database_port: int = Field(5432, env="DATABASE_PORT")

    secret_key: SecretStr = Field(..., env="SECRET_KEY")

    etherscan_api_key: SecretStr = Field(..., env="ETHERSCAN_API_KEY")
    bscscan_api_key: SecretStr = Field(..., env="BSCSCAN_API_KEY")
    polygon_api_key: SecretStr = Field(..., env="POLYGONSCAN_API_KEY")

    etherscan_api_url: str = Field("https://api.etherscan.io/api", env="ETHERSCAN_API_URL")
    bscscan_api_url: str = Field("https://api.bscscan.com/api", env="BSCSCAN_API_URL")
    polygon_api_url: str = Field("https://api.polygonscan.com/api", env="POLYGONSCAN_API_URL")

    rpc_endpoints: Dict[int, str] = Field(..., env="RPC_ENDPOINTS")

    # default chains that always exist
    chains = {
        1: 'Ethereum',
        137: 'Matic',
        56: 'Binance Smart Chain',
    }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
