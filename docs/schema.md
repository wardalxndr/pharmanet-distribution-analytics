# Schema design

Grain-first, star schema. Every mart answers a dashboard question.

## Verified source facts (from scripts/profile_data.py, pharma-data.csv)

- 254,082 rows, 18 columns, zero nulls.
- `Sales == Quantity * Price` on every row (0 mismatches) -> `Sales` is derived;
  keep both columns but add a dbt test asserting the identity.
- 4 exact duplicate rows -> dedup with `SELECT DISTINCT` at staging, documented.
- `Month` is a string month name, `Year` is int -> parse to `sale_date` (DATE,
  first of month) at staging.
- Bonus columns that survive into the model:
  - `Latitude`, `Longitude` (customer location -> geo analysis),
  - `Name of Sales Rep`, `Manager`, `Sales Team` (sales org structure).

## Staging (1:1 with source, typed, renamed, deduped)

- `stg_sales`: one row per unique transaction line, all 18 columns,
  `sale_date` = DATE(first of month from month name + year).

## Dimensional marts

- `dim_distributor` (distributor_id, distributor_name)
- `dim_customer` (customer_id, customer_name, city, country, latitude, longitude)
- `dim_product` (product_id, product_name, product_class)
- `dim_sales_org` (sales_rep_id, sales_rep_name, manager, sales_team)
- `fct_sales` (sale_date, distributor_id, customer_id, product_id,
  sales_rep_id, quantity, unit_price, sales_amount)

## Partitioning and clustering reasoning

- `fct_sales`: PARTITION BY `DATE_TRUNC(sale_date, MONTH)` (monthly partitions:
  big pruning win for every "last N months" dashboard filter; numbers stay
  modest), CLUSTER BY `distributor_id`, `product_id` (top tiles group by
  distributor and class).
- `dim_*` tables are small: no partitioning, cluster optional.

## dbt tests to include

- unique key test on marts' surrogate ids.
- not_null on all facts/dims FKs.
- `sales_amount == quantity * unit_price` accepted-values style check
  (with tolerance) on `fct_sales`.
- source freshness not applicable (static CSV), but row-count sanity vs source
  after load: same row count minus 4 duplicates.

## Phase 2 (optional, do not block phase 1)

- `fct_pos_sales` from the pharmacy POS dataset (sell-out view), joined to
  `dim_product` via product name normalization; sell-in vs sell-out comparison.
- Simulated expiry/stock layer (FEFO, near-expiry exposure) clearly labeled
  as simulated in the README.
- Geo tile: customers plotted by lat/lon (city map) as a bonus dashboard tile.
