# Pharmanet Distribution Analytics

Batch data pipeline and dashboard for pharmaceutical distribution analytics: how a pharma
distributor sells into pharmacies and hospitals, by distributor, region, product class,
and price band. Built as portfolio for data engineering internships.

## Problem description

A pharmaceutical company sells its products through a distributor network into channels
(pharmacy/hospital) and sub-channels. The raw transaction extracts sit in flat files with
no analytics layer, so nobody can answer basic operating questions quickly:

- Which distributors drive revenue, and how is that mix shifting month to month?
- Which product classes (antibiotics, analgesics, antipyretics, ...) grow and which decay?
- Where do we sell: which cities, channels, sub-channels?
- What are we selling and at what price: units, revenue, average price per class?

This project builds the pipeline that answers those questions on a public dataset shaped
like that business (see Data), with a dashboard on top.

> Naming note: "Pharmanet" is the distribution arm concept used as project framing
> (pharma distribution analytics), inspired by how large Indonesian pharma groups
> structure distribution. The data itself is public and NOT from any private company.

## Data

Primary (sell-in): Kaggle "Pharmaceutical Company Wholesale-Retail Data"
(distributor, customer, city, country, channel, sub-channel, product name, product
class, quantity, price, sales, month, year).
https://www.kaggle.com/datasets/krishangupta33/pharmaceutical-company-wholesale-retail-data

Optional (sell-out, phase 2): Kaggle "Pharma sales data" (600k POS transactions,
2014-2019, 57 drugs in 8 ATC categories).
https://www.kaggle.com/datasets/milanzdravkovic/pharma-sales-data

Download with kagglehub or the Kaggle CLI, then place under `data/`.

## Architecture

```
Kaggle CSVs
  -> Airflow (Docker) batch DAG: validate -> upload to GCS datalake
  -> BigQuery RAW (external/load)
  -> dbt: staging -> marts (star schema), partitioned/clustered
  -> Looker Studio dashboard
Infra as code: Terraform (GCS bucket, BQ dataset, service accounts)
```

## Dashboard

Minimum two tiles (zoomcamp rubric), target four:

1. Revenue by product class (categorical, stacked bar).
2. Monthly revenue trend (time series, by distributor).
3. Top customers by revenue (bar/table with filters).
4. Average price per product class (bar, price-mix view).

## Evaluation criteria mapping (DE Zoomcamp)

| Rubric item | How this project addresses it |
| --- | --- |
| Problem description | This README |
| Cloud + IaC | GCP, Terraform for bucket/dataset/SA |
| Workflow orchestration | End-to-end Airflow DAG (data to datalake) |
| Data warehouse | BigQuery, partition + cluster with documented reasoning |
| Transformation | dbt (staging, marts, tests) |
| Dashboard | Looker Studio, 2+ tiles |
| Reproducibility | One-command local run, env vars only, fresh-clone tested |

## Repository layout

```
dags/                 # Airflow DAG: ingest to GCS (-> BQ load)
dbt/                  # dbt project: staging + marts + tests
pipeline/             # (optional) scripts outside the DAG
terraform/            # IaC: GCS, BigQuery, service account
data/                 # downloaded CSVs (gitignored)
docs/                 # schema, dashboard design
.env.example
docker-compose.yml    # Airflow stack
Makefile              # make up / make dbt-run / ...
```

## How to run (draft, finalized as code lands)

1. Create a GCP project, enable BigQuery + Cloud Storage APIs.
2. `cp .env.example .env` (fill project id, credentials path).
3. `terraform apply` to create the bucket, dataset, and service account.
4. `docker compose up` to start Airflow, then trigger the `pharma_ingest` DAG.
5. `dbt run && dbt test` against BigQuery.
6. Open the Looker Studio dashboard (link in docs/dashboard.md).

## License

MIT.
