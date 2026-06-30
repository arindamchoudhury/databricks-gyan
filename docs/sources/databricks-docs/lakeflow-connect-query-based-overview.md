# Query-based connectors (Lakeflow Connect)

> **Source:** [docs.databricks.com/aws/en/ingestion/lakeflow-connect/query-based-overview](https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/query-based-overview)
> **Added:** 2026-06-30
> **Source updated:** 2026-06-10
> **Tags:** lakeflow-connect, query-based-connectors, cursor-column, lakehouse-federation, scd, A3
> **Type:** documentation

**Status:** Public Preview

Query-based connectors ingest from databases by **querying the source directly** — no CDC/binlog configuration required. They use a **cursor column** (monotonically increasing timestamp or integer) to track new or updated rows since the last run.

Uses Unity Catalog connections or Lakehouse Federation foreign catalogs to connect. Writes to streaming tables.

## How it works

On each pipeline run:
1. Queries the source for all rows where `cursor_column > high_water_mark` from the previous run
2. Stores the new high-water mark after each successful run
3. Uses that value as the lower bound on the next run

**No gateway. No staging volume.** Runs on a schedule — not continuously.

## Query-based vs CDC connectors

| | Query-based | CDC (database connector) |
|---|---|---|
| Gateway required | No | Yes |
| Staging volume | No | Yes (UC volume, 30-day purge) |
| Execution | Scheduled | Continuous |
| Intermediate row states | Captures latest state only | Captures every change |
| Source load | Higher (queries source tables directly) | Lower (reads binlog) |
| Source compatibility | Any DB with a cursor column | DB must support CDC/binlog |

**Deletion tracking:**
- Soft deletes: `deletion_condition` (supported)
- Hard deletes: supported (Beta) — both require API configuration

## Two ingestion approaches

### Foreign connection ingestion

Uses a Connection (UC securable with auth credentials) to query the source directly.

Required params: `connection_name`, `source_catalog`, `source_schema`, `source_table`, `cursor_column`

**Supported sources:** Oracle, Teradata, SQL Server, MySQL, MariaDB, PostgreSQL

### Foreign catalog ingestion

Uses a Lakehouse Federation **foreign catalog** instead of a direct connection.

Required params: `ingest_from_uc_foreign_catalog: true`, `cursor_columns`, `primary_keys` (unless using APPEND_ONLY mode)

**Supported sources:** All Lakehouse Federation data sources (full list: see Lakehouse Federation docs)

## Compute

Runs on **serverless** by default. Classic compute: Beta, via DABs or API only. Databricks recommends serverless.

Serverless compute environment must allow network connectivity to the source database.

## History tracking (SCD) modes

Three modes (vs CDC connectors which support only SCD_TYPE_1 and SCD_TYPE_2):

| Mode | Behavior |
|---|---|
| `SCD_TYPE_1` | Overwrites existing row with latest source row; no history |
| `SCD_TYPE_2` | Preserves full row history with version metadata |
| `APPEND_ONLY` | Appends every ingested row without merging or overwriting |

`APPEND_ONLY` does not require `primary_keys`. See [[lakeflow-connect-scd]] for SCD Type 2 details.

## Interfaces

UI + DABs (not CLI-only like some CDC features).

## Schema evolution

Same behavior as other managed connectors — see [[lakeflow-connect-faq]] schema evolution section.

[[lakeflow-connect-managed]] · [[lakeflow-connect-cdc-overview]] · [[lakeflow-connect-scd]] · [[lakeflow-connect-faq]]
