# Materialized views (and the serverless compute model)

> **Source:** [docs.databricks.com/aws/en/ldp/concepts/materialized-views](https://docs.databricks.com/aws/en/ldp/concepts/materialized-views) · [ldp/dbsql/materialized](https://docs.databricks.com/aws/en/ldp/dbsql/materialized)
> **Added:** 2026-06-25
> **Source updated:** 2026-06-16 (concepts) / 2026-06-15 (standalone)
> **Tags:** materialized-view, lakeflow, declarative-pipelines, serverless, dbsql, incremental-refresh, row-tracking, federation, I3, I8, A7
> **Type:** documentation

## Summary

A **materialized view (MV)** is a Lakeflow Spark Declarative Pipelines object: it caches a query's results as a UC managed table and refreshes them (often incrementally) on a trigger or schedule, so reads are far faster than a recomputed standard view. The compute story is the key gotcha: **create and refresh always run on an auto-created *serverless* pipeline**, billed as serverless Lakeflow Spark Declarative Pipelines DBUs — *regardless* of the SQL warehouse or notebook you submitted from. You can *invoke* the statement from a Pro/Serverless SQL warehouse or a serverless notebook, but the data processing itself is serverless and you can't point it at a classic cluster.

## Key points

- **MV = declarative-pipeline object.** It bundles a defining query, a flow that updates it, and the cached results. Defined and updated by exactly one pipeline; no other pipeline can modify it.
- **Standalone MV** (defined outside a pipeline via Databricks SQL `CREATE MATERIALIZED VIEW`) is a **UC managed table**. Databricks auto-creates a pipeline behind it (visible under **Jobs & Pipelines**, **Pipeline type = MV/ST**; pipeline-defined MVs show type `ETL`).
- **Create/refresh always runs on a serverless pipeline.** "A serverless pipeline is automatically created for every standalone materialized view." The warehouse only *coordinates/monitors*; the warehouse cluster size does **not** cap the refresh compute or cost.
- **You can incur serverless charges even when the originating warehouse uses dedicated compute.** Cost scales with data processed, not warehouse size.
- **Where you can submit from:** a **Databricks SQL warehouse** (must be **Pro or Serverless** for federation sources — Classic isn't supported) **or** a **notebook on serverless general compute**. (See "Requirements for standalone pipelines".)
- **Standalone MVs always run in triggered mode** (never continuous).
- **Refresh = incremental or full.** A cost model picks the cheaper; override with `REFRESH POLICY`. Incremental requires **Delta sources with row tracking + change data feed enabled** (`delta.enableRowTracking = true`). Check with `EXPLAIN CREATE MATERIALIZED VIEW`.
- **Federation tie-in:** MVs can be built on external data via Lakehouse Federation — this is the recommended way to *replicate a foreign table into UC* (`CREATE MATERIALIZED VIEW … AS SELECT * FROM federated_catalog.federated_schema.federated_table`).

## Notes

### Compute / serverless requirement (the actual answer to "is it serverless-only?")

- **Effectively yes for standalone MVs.** The create + every refresh run on a serverless Lakeflow SDP pipeline. There is no option to run that processing on classic compute.
- **The entry point isn't serverless-restricted:** submit from a Pro/Serverless **SQL warehouse** (SQL editor, SQL CLI, SQL API, or a notebook attached to the warehouse) or from a **serverless notebook** (Python via `from pyspark import pipelines as dp`). The warehouse/notebook just kicks off and watches the serverless pipeline.
- **Prerequisite:** serverless Lakeflow pipelines must be **available/enabled in your workspace and region**. If serverless isn't available to you, the standalone-MV path effectively isn't either.
- **Exception — MVs inside a *regular* Declarative Pipeline:** those follow the pipeline's compute, and pipelines can run on **serverless or classic**. So "MV always = serverless" is true for the *standalone/DBSQL* path (the federation→replication recommendation), not for an MV authored inside a classic pipeline.

### Trigger / schedule options (standalone)

- **Ad-hoc:** `CREATE OR REPLACE MATERIALIZED VIEW mv AS SELECT …` — initial load runs immediately on the serverless pipeline (does not consume warehouse compute).
- **On update:** `… TRIGGER ON UPDATE` — auto-refresh whenever upstream source data changes (recommended for production with unpredictable upstreams).
- **Scheduled:** `… SCHEDULE CRON '0 30 3 * * ?' AT TIME ZONE 'UTC'` (or `SCHEDULE EVERY …`).
- **Refresh:** `REFRESH MATERIALIZED VIEW mv;` (synchronous by default; add `ASYNC` to return immediately and run the load on background serverless compute, allowing parallel refreshes and letting the warehouse shut down).

### Incremental vs full refresh

Incremental merges only changes since the last update; full reruns the whole query and replaces data. Incremental support depends on query structure + source type (Delta + row tracking + CDF). Re-enabling row tracking is required if you recreate a source table.

## Quotes worth keeping

> "When you create a materialized view in a Databricks SQL warehouse, a serverless pipeline is created to process the create and refreshes to the materialized view." (standalone MV — What are standalone MVs)

> "The refresh pipeline runs on serverless compute, billed as serverless Lakeflow Spark Declarative Pipelines DBUs. … The cluster size of your warehouse does not limit the compute or cost used by the refresh." (Understand the costs)

> "You might incur serverless compute charges even when the originating warehouse uses dedicated compute." (Understand the costs — note)

## Open questions

- The exact serverless availability matrix (which workspaces/regions) lives on "Requirements for standalone pipelines" (`ldp/dbsql/compute`) — not yet captured.

## Related sources

- [[serverless-pipelines]] — serverless compute for Lakeflow pipelines (modes, DBU trade-off, serverless-exclusive features); the engine MVs run on.
- [[foreign-tables]] — replicating a foreign table into UC via an MV is the federation→managed migration path.
- [[external-access]] — accessing an MV from external Delta/Iceberg clients uses Compatibility Mode (read-only copy).
- [[row-tracking]] — the substrate incremental MV refresh depends on.
