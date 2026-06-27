# Serverless compute for Lakeflow Spark Declarative Pipelines

> **Source:** [docs.databricks.com/aws/en/ldp/serverless](https://docs.databricks.com/aws/en/ldp/serverless)
> **Added:** 2026-06-16
> **Source updated:** 2026-06-22
> **Tags:** serverless, pipelines, lakeflow, ldp, dlt, compute, performance-modes, I5
> **Type:** documentation

Serverless pipelines run Lakeflow Spark Declarative Pipelines (formerly Delta Live Tables) on Databricks-managed infrastructure — no cluster configuration. **Unity Catalog is required**, and any existing cluster config is removed when serverless is enabled. Databricks recommends serverless for all **new** pipeline development; the exception is workloads that require classic compute or the legacy Hive metastore. Pipeline modes — **triggered, continuous, and real-time** — are all supported, and the Structured Streaming *trigger* limitations from [[serverless-limitations]] (AvailableNow/Once only) **do not apply** to pipeline modes.

## Requirements

UC-enabled workspace; user accepts serverless terms; supported serverless region. **No cluster-creation permission needed** — all workspace users can configure serverless pipelines by default.

## Configuration options

Pipeline mode (Triggered / Continuous / Real-time); email notifications; a key-value **Configuration field** (referenceable in source + Spark config); **Preview channel** (test pending runtime changes); **Environment settings** (external Python deps); and **serverless usage policy** *(Public Preview)* for billing-attribution tags.

> ⚠️ `dbutils.library.restartPython()` is **not supported** in serverless pipelines.

## Converting an existing pipeline to serverless

**Jobs & Pipelines** → pipeline name → **Settings** → under **Compute** click the pencil → check **Serverless** → **Save**.

> ⚠️ "When you enable serverless, any compute settings you have configured for a pipeline are removed." Any `clusters` config in the pipeline JSON is discarded; switching back requires reconfiguring from scratch.

## Performance modes (triggered pipelines only)

Same SKU for both; the difference is startup latency and DBU consumption:

| Mode | Startup | DBU use | Best for |
|---|---|---|---|
| **Standard** | 4–6 min | Lower | Cost-sensitive, latency-tolerant pipelines |
| **Performance Optimized** | Fast | Higher | Time-sensitive, SLA-bound pipelines |

> 💡 Same two modes as [[serverless-jobs]]. Performance mode is selected per *triggered* pipeline via the **Performance optimized** toggle (off = standard). Continuous pipelines default to performance-optimized; using **standard** mode on continuous pipelines requires contacting your Databricks account team.

## Serverless-exclusive features

Three capabilities not available on classic clusters:

- **Incremental refresh** — materialized views refresh incrementally whenever possible (full-refresh fallback).
- **Stream pipelining** — microbatches run concurrently instead of sequentially, improving resource utilisation. On by default.
- **Vertical autoscaling** — *adds to* horizontal autoscaling by allocating the most cost-efficient instance types that run the pipeline without OOM.

## Monitoring costs

Query the **billable usage system table** to track serverless pipeline DBU consumption (same approach as [[serverless-jobs]]).

Related: [[serverless-jobs]], [[serverless-notebooks]], [[serverless-limitations]], [[data-engineering-hub]], [[materialized-views]].
