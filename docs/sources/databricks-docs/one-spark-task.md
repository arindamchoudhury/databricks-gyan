# One Spark Task

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/one-spark-task](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/one-spark-task)
> **Added:** 2026-06-17
> **Source updated:** 2024-08-26
> **Tags:** spark, spark-ui, debugging, tasks, parallelism, UDF, gzip, coalesce, repartition, B2, B16
> **Type:** documentation

A sub-page of the Spark UI Guide series, reached from Step 2 when a stage has exactly one task — one CPU doing all the work while the rest of the cluster idles.

> "If you see a long-running stage with just one task, that's likely a sign of a problem. While this one task is running only one CPU is utilized and the rest of the cluster may be idle."

## Six causes

| # | Cause | Notes |
|---|---|---|
| 1 | **Expensive UDF on small data** | UDF forces single-partition execution; see UDF docs for native rewrites |
| 2 | **Window function without `PARTITION BY`** | Entire dataset in one partition; always add `PARTITION BY` on a useful key |
| 3 | **Unsplittable file type** (e.g. Gzip) | Gzip can't be split across tasks; use Snappy or LZ4, or re-compress |
| 4 | **`multiLine` option on JSON/CSV** | Forces single-task read; avoid `multiLine=true` on large files |
| 5 | **Schema inference on large file** | Spark reads the whole file once to infer schema; provide schema explicitly |
| 6 | **`repartition(1)` or `coalesce(1)`** | Explicitly collapses to one partition; remove from production code unless intentional |

Related: [[spark-ui-guide]], [[long-spark-stage]], [[spark-memory-issues]].
