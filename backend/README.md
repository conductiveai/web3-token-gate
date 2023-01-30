# Conductive Web3 Token Gate Backend

It preforms tasks such as wallet ownership verification, jwt generation
and managing user profile data.

## Deploying to GCP
1. In secret manager, define all secrets you see in [cloudbuild.yml](/backend/cloudbuild.yml) such as 
    * `WTG_DB_HOST`
    * `WTG_DB_PORT`
    * `WTG_DB_USER`
    * `WTG_DB_PASSWORD`
    * `WTG_DB_NAME`
    * `WTG_POLYGONSCAN_API_KEY` (leave blank if you are not planning to use polygon)
    * `WTG_ETHERSCAN_API_KEY` (leave blank if you are not planning to use ethereum mainnet)
    * `WTG_BSCSCAN_API_KEY` (leave blank if you are not planning to use binance smart chain)
    * `WTG_APP_SECRET_KEY` (any secure random string, will be used for jwt signing)
2. Create a Cloud bucket for frontend
3Create a GCP trigger and specify path to [backend/cloudbuild.yml](/backend/cloudbuild.yml), in substitute variables section specify `_SERVICE_ACCOUNT`. If you are planning to connect to the database by private IP, also specify `_VPC_CONNECTOR`
3. Create a GCP trigger and specify path to [frontend/cloudbuild.yml](/frontend/cloudbuild.yml), in substitute variables section add `_FE_BUCKET_NAME` with cloud bucket name in it

## Running code locally

You can run the code locally with the following command:

```bash
uvicorn main:create_app --reload --factory
```

## Endpoints

All of the available endpoints are self documented here: /docs

## Running tests

```bash
docker compose -f tests-docker-compose.yml up --build
```
