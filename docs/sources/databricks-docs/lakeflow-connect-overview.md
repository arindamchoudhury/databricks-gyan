# What is Lakeflow Connect?

> **Source:** [docs.databricks.com/aws/en/ingestion/overview](https://docs.databricks.com/aws/en/ingestion/overview)
> **Added:** 2026-06-29
> **Source updated:** 2026-06-03
> **Tags:** ingestion, lakeflow-connect, managed-connectors, standard-connectors, community-connectors, auto-loader, kafka, etl, incremental, A3, I1
> **Type:** documentation

Lakeflow Connect is the umbrella for all Databricks ingestion tooling: fully-managed connectors for enterprise apps and databases, standard connectors for cloud storage and message buses, community connectors, and file upload. It uses UC for governance, Lakeflow Jobs for orchestration, and holistic monitoring across pipelines.

## Service models

Two levels of customization:

| Option | Description |
|---|---|
| Fully-managed | Out-of-the-box connectors via UI, API, SDK, CLI, or DABs — minimal long-term maintenance |
| Custom pipeline | Lakeflow Spark Declarative Pipelines (SDP) or Structured Streaming for full control |

## ETL stack layers

Databricks recommends starting at the most managed layer and dropping down only if your source isn't supported:

| Layer | Description |
|---|---|
| **Fully-managed connectors** (most managed) | Built on SDP; add source-specific auth, CDC, edge-case handling, automated retries, and schema evolution for each supported source |
| **Lakeflow Spark Declarative Pipelines** | Declarative framework built on Structured Streaming. For any Structured Streaming feature not yet in SDP, use the SS APIs directly |

The fully-managed layer is a superset of SDP — it handles everything SDP does plus source-specific concerns.

## Connector types

**Managed connectors** — enterprise apps (Salesforce, ServiceNow) and databases (SQL Server, MySQL via CDC). Accessible via UI, declarative automation bundles, Databricks APIs/SDKs/CLI.

**Community connectors** — built and maintained by the community; no Databricks SLA. Use an existing one or create your own.

**Standard connectors** — cloud object storage and message buses (Kafka, Kinesis, Pub/Sub, Pulsar) with more customization options. Includes Auto Loader (`cloudFiles`) for cloud storage.

**File upload (Add data UI)** — ingest local files, files on a volume, or files from a URL.

## Ingestion partners and DIY

Third-party tools (validated by Databricks): Fivetran, Airbyte, and others in Partner Connect. For DIY ingestion, any language supported by Databricks works; popular open-source libraries include dlt, Airbyte, and Debezium.

## Performance

Lakeflow Connect uses **incremental reads and writes**. Combined with [incremental transformations downstream](https://docs.databricks.com/aws/en/optimizations/incremental-refresh), this can significantly improve overall ETL performance.

## When NOT to ingest (alternatives)

Ingestion copies data, which means duplicate data that can go stale. If you don't want to copy:

| Tool | Use case |
|---|---|
| Lakehouse Federation | Query external sources in place — no copy |
| OpenSharing | Share data across platforms, clouds, or regions — no copy |

[data-engineering-hub](data-engineering-hub/) · [serverless-pipelines](serverless-pipelines/) · [batch-vs-streaming](batch-vs-streaming/)
