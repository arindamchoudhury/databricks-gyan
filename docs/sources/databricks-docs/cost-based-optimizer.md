# Cost-based optimizer (CBO)

> **Source:** [docs.databricks.com/aws/en/optimizations/cbo](https://docs.databricks.com/aws/en/optimizations/cbo)
> **Added:** 2026-06-24
> **Source updated:** 2025-02-04
> **Tags:** optimization, performance, cbo, cost-based-optimizer, statistics, analyze-table, joins, explain, predictive-optimization, A1
> **Type:** documentation

Spark SQL's cost-based optimizer (CBO) improves query plans — especially join order/strategy — using **table and column statistics**. Default-on (`spark.sql.cbo.enabled = true`), and it's especially valuable for queries with **multiple joins** (`rowCount` drives join planning).

> "For this to work it is critical to collect table and column statistics and keep them up to date."

On UC managed tables, **predictive optimization runs `ANALYZE` automatically**, so stats stay fresh without manual work ([[predictive-optimization]]).

## Collect statistics

```sql
ANALYZE TABLE <table-name> COMPUTE STATISTICS FOR ALL COLUMNS
```

Run it after writing to a table to keep stats current.

## Verify query plans — `EXPLAIN`

`EXPLAIN` shows whether the plan uses stats. Each operator carries `Statistics(sizeInBytes=…, rowCount=…)`.

> "The rowCount statistic is especially important for queries with multiple joins. If rowCount is missing, it means there is not enough information to calculate it…"

[![Missing estimate — no stats](assets/cost-based-optimizer/01-missing-estimate.png)](assets/cost-based-optimizer/01-missing-estimate.png)
*Missing estimate: operator has no stats available.*

[![Good estimate](assets/cost-based-optimizer/02-good-estimate.png)](assets/cost-based-optimizer/02-good-estimate.png)
*Good estimate: estimated rows ≈ actual, error factor ~1.*

[![Bad estimate](assets/cost-based-optimizer/03-bad-estimate.png)](assets/cost-based-optimizer/03-bad-estimate.png)
*Bad estimate: estimate off by ~1000× — stale/missing stats.*

DBR 16.0+ `EXPLAIN` adds a stats-state summary:

```text
== Optimizer Statistics (table names per statistics state) ==
  missing = date_dim, store
  partial =
  full    = store_sales
Corrective actions: consider running the following command on all tables with missing or partial statistics
  ANALYZE TABLE <table-name> COMPUTE STATISTICS FOR ALL COLUMNS
```

In the Spark SQL UI, each operator shows estimate accuracy: `est: N/A` (no stats), `est: 1616404 (1X)` (good, error factor 1), or an estimate off by ~1000× (bad).

## Disable

```scala
spark.conf.set("spark.sql.cbo.enabled", false)
```

Related: [[predictive-optimization]], [[aqe]], [[optimization-recommendations]].
