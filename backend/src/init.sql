DROP MATERIALIZED VIEW IF EXISTS "public"."wallet_balances";
CREATE MATERIALIZED VIEW "public"."wallet_balances" AS (

WITH tx AS (
    SELECT
        lower(from_address) AS "address",
        contract.chain_id as chain,
        contract.id as contract_id,
        transaction.token_id as token_id,
        CASE WHEN lower(to_address) = '0x0000000000000000000000000000000000000000' THEN 1  ELSE NULL END as is_burn,
        NULL as is_mint,
        CASE
        WHEN contract.erc_standard = 721 THEN
            -1
        ELSE
            -"value"
        END AS "balance",
        "timestamp"
    FROM "public"."transaction"
    INNER JOIN "public"."contract" on transaction.contract_id = contract.id
    UNION ALL
    SELECT
        lower(to_address) AS "address",
        contract.chain_id as chain,
        contract.id as contract_id,
        transaction.token_id as token_id,
        NULL as is_burn,
        CASE WHEN lower(from_address) = '0x0000000000000000000000000000000000000000' THEN 1  ELSE NULL END as is_mint,
        CASE
        WHEN contract.erc_standard = 721 THEN
            1
        ELSE
            "value"
        END AS "balance",
        "timestamp"
    FROM "public"."transaction"
    INNER JOIN "public"."contract" on transaction.contract_id = contract.id and transaction.chain_id = contract.chain_id
)
SELECT
    address as address,
    chain as chain_id,
    contract_id,
    token_id,
    SUM(tx.balance) as balance,
    MAX(tx.timestamp) as date
FROM tx WHERE address NOT IN ('0x0000000000000000000000000000000000000000')
GROUP BY 1,2,3,4
ORDER BY date DESC

) WITH DATA;

-- create a unique index on the materialized view
CREATE UNIQUE INDEX "unq_wallet_contract" ON "public"."wallet_balances" ("address", "contract_id", "chain_id", "token_id");
