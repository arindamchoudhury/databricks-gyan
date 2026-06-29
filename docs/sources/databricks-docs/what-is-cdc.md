# Change data capture and snapshots

> **Source:** [docs.databricks.com/aws/en/data-engineering/what-is-cdc](https://docs.databricks.com/aws/en/data-engineering/what-is-cdc)
> **Added:** 2026-06-29
> **Source updated:** 2026-06-10
> **Tags:** data-engineering, cdc, change-data-capture, snapshots, scd, scd-type-1, scd-type-2, auto-cdc, lakeflow, streaming-tables, delta, I4, I2
> **Type:** documentation

**Change data capture (CDC)** treats a database as a set of changes rather than a complete static snapshot. The challenge: source systems expose changes in different formats — some emit per-row change feeds (insert/update/delete), others only provide periodic full-table snapshots. The page covers both formats and maps them to Databricks' two `AUTO CDC` APIs.

## What are the benefits of CDC?

- **Smaller data volumes** — only changes, not full tables, flow downstream.
- **Full history** — changes can be stored to reconstruct records as they were at any point in time (auditing, point-in-time reporting, trend analysis).
- **Stable surrogate keys** — keys are preserved across changes rather than reassigned on reload.

## How changes are applied: SCD Type 1 and Type 2

**Slowly Changing Dimensions (SCD)** define how upstream changes land in analytical tables.

### SCD Type 1 — Current state only

Overwrites old data with new data; no history retained. The table always reflects only the latest version of each record.

Use when:
- Only the current state of the data is needed.
- Downstream materialized views should incrementally refresh (not fully recompute).
- Stable surrogate keys are required for joins.

### SCD Type 2 — Historical tracking

Creates multiple versioned rows per record, each with `__START_AT` and `__END_AT` validity columns. Active (current) records have `__END_AT = NULL`.

Use when:
- Auditability or regulatory requirements demand a full history.
- Customer analytics needs to understand how entities evolved.
- Business logic requires point-in-time reporting or trend comparison.

## What is a CDC feed?

A CDC feed captures individual row-level changes (INSERT, UPDATE, DELETE) from a source system. Each record includes:

- **Operation type** — `INSERT`, `UPDATE`, or `DELETE`
- **Data values** for the record
- **Sequence number or timestamp** — for deterministic ordering (handles out-of-order arrivals)

Transactional databases (SQL Server, MySQL, Oracle) generate CDC feeds natively. Delta tables also generate a **Change Data Feed (CDF)**, making it straightforward to process changes from Delta sources.

## What is a snapshot?

A snapshot is the **complete state of a table at a specific point in time** — every row, not just changes. Teams use snapshot-based ingestion when CDC feeds are unavailable due to cost, performance concerns, legacy system constraints, or organizational ownership gaps.

Snapshot sources include: periodic DB exports, cloud storage file dumps, Delta table versions, OpenSharing from upstream tenants.

Because snapshots don't capture record-level changes, identifying what changed requires **comparing consecutive snapshots** to infer inserts, updates, and deletes.

## Automatically process CDC feeds — `AUTO CDC`

Databricks' `AUTO CDC` API in **Lakeflow Spark Declarative Pipelines** processes changes from CDC feeds on source databases or Delta tables with CDF enabled.

Use `AUTO CDC` when:
- The source generates a Change Data Feed (CDF)
- Reading from a Delta table with CDF enabled
- You have a CDC feed from a relational DB (via Debezium, Oracle GoldenGate, etc.)

Key behaviors:
- Handles **out-of-sequence records** automatically using a monotonically-increasing sequencing column (`NULL` sequencing values not supported)
- For SCD Type 2, sequencing values propagate to `__START_AT` / `__END_AT`
- **Initial hydration**: use *once flows* to load all historical data first, then switch to triggered/continuous mode for ongoing CDC

## Automatically process snapshots — `AUTO CDC FROM SNAPSHOT`

When CDC feeds aren't available, `AUTO CDC FROM SNAPSHOT` compares **consecutive snapshots**, generates a synthetic change feed, and applies SCD Type 1 or Type 2 logic. **Python pipeline interface only.**

Use when:
- CDC is not enabled on the source
- Only periodic full table dumps are available
- You want CDC benefits (incremental processing, stable keys, full history) without a native feed

What it handles automatically:
1. Compares consecutive snapshots to identify inserts, updates, and deletes
2. Generates a synthetic change feed from the diff
3. Applies the same SCD logic as `AUTO CDC`

> ⚠️ `AUTO CDC FROM SNAPSHOT` only sees changes **between snapshots** — interim changes within a period are lost. With daily snapshots, two address changes in one day (A→B→C) collapse to A→C.

Snapshots must be processed in **ascending order by version**; out-of-order snapshots are ignored.

### Two snapshot processing patterns

**By pipeline ingestion time** — snapshot is read at pipeline run time; ingestion timestamp = version. Use when snapshots arrive regularly and in order.

**By version function** — you provide a function returning `(DataFrame, version_number)`. The API processes snapshots in version order. Use when multiple snapshots arrive simultaneously, arrive out of order, or you need explicit ordering control.

## Additional capabilities

| Capability | Detail |
|---|---|
| DML on `AUTO CDC` targets | Unity Catalog `AUTO CDC` target tables support `INSERT`, `UPDATE`, `DELETE`, `MERGE` while the pipeline runs |
| CDF from `AUTO CDC` targets | `AUTO CDC` output tables can emit their own CDF for downstream pipelines |
| Metrics | `num_upserted_rows` and `num_deleted_rows` captured automatically per run |
| SCD Type 2 column subset | Specify which columns trigger new history versions; untracked column changes update the current version in place (reduces storage + query complexity) |

## Recommendations

| Situation | Use |
|---|---|
| Source emits a change feed (CDC-enabled DB, Delta CDF) | `AUTO CDC` |
| Source only provides periodic full table dumps | `AUTO CDC FROM SNAPSHOT` |
| Only need current state | SCD Type 1 |
| Need full history / audit trail / point-in-time | SCD Type 2 |

Related: [[change-data-feed]], [[batch-vs-streaming]], [[materialized-views]], [[streaming-tables]], [[procedural-vs-declarative]].
