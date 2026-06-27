# Materialized views (and the serverless compute model)

> **Source:** [docs.databricks.com/aws/en/ldp/concepts/materialized-views](https://docs.databricks.com/aws/en/ldp/concepts/materialized-views) · [ldp/dbsql/materialized](https://docs.databricks.com/aws/en/ldp/dbsql/materialized)
> **Added:** 2026-06-25
> **Source updated:** 2026-06-16 (concepts) / 2026-06-15 (standalone)
> **Tags:** materialized-view, lakeflow, declarative-pipelines, serverless, dbsql, incremental-refresh, row-tracking, federation, I3, I8, A7
> **Type:** documentation

A **materialized view (MV)** is a Lakeflow Spark Declarative Pipelines object: it caches a query's results as a UC managed table and refreshes them (often incrementally) on a trigger or schedule, so reads are far faster than a recomputed standard view. An MV bundles a defining query, a flow that updates it, and the cached results; it's defined and updated by exactly **one** pipeline.

The compute story is the key gotcha:

> "When you create a materialized view in a Databricks SQL warehouse, a serverless pipeline is created to process the create and refreshes… The cluster size of your warehouse does not limit the compute or cost used by the refresh."

So **create + refresh always run on an auto-created *serverless* pipeline** (billed as serverless Lakeflow SDP DBUs), regardless of the warehouse/notebook you submitted from — and "you might incur serverless compute charges even when the originating warehouse uses dedicated compute."

## Compute / serverless requirement

- **Effectively serverless-only for standalone MVs.** The create + every refresh run on a serverless Lakeflow SDP pipeline; there's no option to run that processing on classic compute. A standalone MV (`CREATE MATERIALIZED VIEW` in Databricks SQL) is a **UC managed table** with an auto-created pipeline behind it (visible under **Jobs & Pipelines**, type **MV/ST**; pipeline-defined MVs show type `ETL`).
- **The entry point isn't serverless-restricted:** submit from a **Pro/Serverless SQL warehouse** (Classic isn't supported for federation sources) or a **serverless notebook** (`from pyspark import pipelines as dp`). The warehouse/notebook just kicks off and watches the serverless pipeline.
- **Prerequisite:** serverless Lakeflow pipelines must be available in your workspace/region.
- **Exception — MVs inside a *regular* pipeline** follow that pipeline's compute (serverless **or** classic). So "MV always = serverless" holds for the standalone/DBSQL path, not for an MV authored inside a classic pipeline.

## Trigger / schedule options (standalone)

Standalone MVs always run in **triggered** mode (never continuous):

```sql
CREATE OR REPLACE MATERIALIZED VIEW mv AS SELECT … ;          -- ad-hoc; initial load runs on the serverless pipeline
… TRIGGER ON UPDATE ;                                         -- auto-refresh when upstream changes
… SCHEDULE CRON '0 30 3 * * ?' AT TIME ZONE 'UTC' ;           -- or SCHEDULE EVERY …
REFRESH MATERIALIZED VIEW mv ;                                -- synchronous; add ASYNC to return immediately
```

## Incremental vs full refresh

A cost model picks the cheaper of incremental (merge only changes since last update) vs full (rerun + replace); override with `REFRESH POLICY`. **Incremental requires Delta sources with row tracking + change data feed enabled** (`delta.enableRowTracking = true`); check with `EXPLAIN CREATE MATERIALIZED VIEW`. Re-enable row tracking if you recreate a source table.

## Federation tie-in

MVs can be built on external data via Lakehouse Federation — the recommended way to **replicate a foreign table into UC**: `CREATE MATERIALIZED VIEW … AS SELECT * FROM federated_catalog.federated_schema.federated_table`.

Related: [[serverless-pipelines]], [[foreign-tables]], [[external-access]], [[row-tracking]], [[data-engineering-hub]].
