# Conductive Token Check Backend

preform tasks such as verifying ownership of wallet, generation of jwt
and managing user profile data.

## Deploying to GCP
1. In secret manager, define all secrets you see in [cloudbuild.yml](/backend/cloudbuild.yml) such as 
    * `CTC_DB_HOST`
    * `CTC_DB_PORT`
    * `CTC_DB_USER`
    * `CTC_DB_PASSWORD`
    * `CTC_DB_NAME`
    * `CTC_POLYGONSCAN_API_KEY` (leave blank if you are not planning to use polygon)
    * `CTC_ETHERSCAN_API_KEY` (leave blank if you are not planning to use ethereum mainnet)
    * `CTC_BSCSCAN_API_KEY` (leave blank if you are not planning to use binance smart chain)
    * `CTC_APP_SECRET_KEY` (any secure random string, will be used for jwt signing)
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
