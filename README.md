# Conductive web3 Token Gate

---

Conductive web3 Token Gate is a service that allows any user holding your token in a wallet to submit their profile.
The service will verify that the user owns the wallet and then store the profile data in a database, 
from where it can be accessed by your application later, or exported directly.

The service provides a way to filter tokens by ID or by held quantity.

Frontend included with service has some options for customization, but you are not limited to it.
You can use your own frontend or integrate the service with your existing application, using [the API](/frontend/src/tokencheck/index.js).

---

## Deployment

Code can be run in two ways:

1. Using docker-compose
     ```
     docker-compose up
     ```
2. Using Google Cloud Functions
    There are `cloudbuild.yml` files in each directory. 
    You can use them to deploy the function to Google Cloud Functions, 
    and upload built files to Google Cloud Storage. 
    Read more about it [here](./backend/README.md#deploying-to-gcp).

When running locally or in docker, specify environment variables in `backend/.env`:

    DATABASE_NAME=...
    DATABASE_USER=...
    DATABASE_PASSWORD=...
    DATABASE_HOST=...
    DATABASE_PORT=...
    SECRET_KEY=... (any secure random string, will be used for jwt signing)
    ETHERSCAN_API_KEY=... (leave blank if you are not planning to use ethereum mainnet)
    BSCSCAN_API_KEY=... (leave blank if you are not planning to use binance smart chain)
    POLYGONSCAN_API_KEY=... (leave blank if you are not planning to use polygon)
    RPC_ENDPOINTS={"1": "https://..."} (map chain id to RPC url)

## Database initialization

Database migrations can be applied with the following command:

    docker-compose run --rm backend pem migrate

Postgres materialized views can be created with the following command:

    docker-compose run --rm backend python run_command.py init-views

## Vocabulary

### Context
Context is a combination of organization and smart contract. Each context will have its own verification link,
and its own set of rules, such as token ID whitelist, token threshold, etc.

### Organization
Organization is a group of people, that can be identified by its name. Each organization can have multiple contexts.

### Token ID Whitelist
list of token IDs that are required to be present in the wallet to submit a profile. In case it is empty, 
any token ID is allowed.

### Token Threshold
Minimum amount of tokens that are required to be present in the wallet to submit a profile.


### Context String Templates
Some text that is displayed in the form may be changed. There are substitute variables available for those templates. 

`{balance}` - total balance of token (across all IDs for 721/1155),

`{threshold}` - token threshold in this context

`{claimable_balance}` - balance across whitelisted IDs if there are any, if not, equal to `{balance}`

## Permissions and roles

There are 4 roles in the system:

- superadmin
- admin
- user
- anonymous user

### Superadmin

superadmin can create and manage organizations. It includes editing list of admins and contexts.

### Admin

admin can only view analytical data in the dashboard and export verified user profiles as CSV.

### User

User is any verified visitor of the website that connected a wallet. User can submit a profile if they have
enough required tokens in wallet.

### Anonymous user

Anonymous user is any visitor of the website that didn't connect a wallet. Anonymous user can't do much 
except for connecting a wallet and becoming one of the above roles.