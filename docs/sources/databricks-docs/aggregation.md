# Aggregate data on Databricks

> **Source:** [docs.databricks.com/aws/en/transform/aggregation](https://docs.databricks.com/aws/en/transform/aggregation)
> **Added:** 2026-06-29
> **Source updated:** 2026-03-12
> **Tags:** data-engineering, aggregation, batch, stateful, stateful-aggregates, watermarks, materialized-views, incremental, approximate, approx_count_distinct, tablesample, I2, I3, I5
> **Type:** documentation

The page taxonomises Databricks aggregation into four categories — **batch**, **stateful**, **incremental**, and **approximate** — and gives the key recommendation: use **materialized views** for incrementally updated pre-computed aggregates rather than repeated batch queries or stateful streaming.

## Batch aggregates

The default behavior for ad hoc SQL queries and Spark DataFrame operations. Every run computes aggregate statistics over **all records** in the data source. Databricks applies optimizations and metadata where possible.

**Downside:** latency and compute cost grow with data size. Pre-computed, frequently-referenced aggregates should use materialized views instead.

## Stateful aggregates

Aggregates defined in **streaming workloads** are stateful — they track observed records over time and recompute when new data arrives.

**Watermarks are required.** Omitting a watermark from a stateful aggregate query causes state to accumulate infinitely, producing slowdowns and eventually OOM errors.

Stateful aggregates are **not suited** for computing statistics over an entire dataset — use incremental aggregates (materialized views) for that.

Configuring stateful aggregates efficiently requires understanding: how data arrives from source systems, how Databricks uses **watermarks**, **output modes**, and **trigger intervals** to control query state and result computation.

## Incremental aggregates

**Materialized views** compute aggregate values incrementally. They automatically track source changes and apply appropriate updates on each refresh. Results are equivalent to a full batch recompute but computed incrementally.

This is the **recommended approach** for pre-computed aggregates that are queried frequently.

## Approximate aggregates

Approximation trades precision for speed and lower cost on very large datasets.

> `LIMIT` is not sufficient — it doesn't introduce randomness or guarantee distributed sampling.

Native Spark SQL approximate functions:

| Function | Purpose |
|---|---|
| `approx_count_distinct` | Approximate distinct count |
| `approx_percentile` | Approximate percentile |
| `approx_top_k` | Approximate top-K |

Use `TABLESAMPLE` to generate a **random sample** from a dataset and calculate approximate aggregates over it.

## Monitor datasets using aggregate statistics

Data profiling uses aggregate statistics and distributions to track **data quality over time**. Reports visualise trends; scheduled alerts flag unexpected changes. See [Data profiling](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/).

## Decision guide

| Situation | Use |
|---|---|
| One-off query over full dataset | Batch aggregate |
| Frequently queried pre-computed result | Materialized view (incremental) |
| Real-time streaming stats over a window | Stateful aggregate (with watermark) |
| Large data, fast, "good enough" answer | Approximate aggregate (`approx_*` / `TABLESAMPLE`) |

Related: [[batch-vs-streaming]], [[materialized-views]], [[procedural-vs-declarative]], [[schema-evolution]].
