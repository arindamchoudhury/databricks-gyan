# One Spark Task

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/one-spark-task](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/one-spark-task)
> **Added:** 2026-06-17
> **Source updated:** 2024-08-26
> **Tags:** spark, spark-ui, debugging, tasks, parallelism, UDF, gzip, coalesce, repartition, B2, B16
> **Type:** documentation

## Summary

Sub-page of the Spark UI Guide series, reached from Step 2 when a stage has exactly one task. One task means one CPU doing all the work while the rest of the cluster idles. Lists six causes — page is a diagnostic index only; each cause links out to specific docs.

## Key points

- One task in a stage = almost certainly a problem (full cluster idle except one CPU).
- Six causes: UDF on small data, unbounded window, unsplittable format (Gzip), `multiLine` option, schema inference, explicit `repartition(1)`/`coalesce(1)`.
- Unsplittable formats and `multiLine` both force a single reader — restructure files or remove the option to fix.
- `repartition(1)`/`coalesce(1)` in the pipeline code is the simplest fix — just remove it.

## Notes

### Why one task is a problem

> "If you see a long-running stage with just one task, that's likely a sign of a problem. While this one task is running only one CPU is utilized and the rest of the cluster may be idle."

### Six causes

| # | Cause | Notes |
|---|---|---|
| 1 | **Expensive UDF on small data** | UDF forces single-partition execution; see UDF docs for native rewrites |
| 2 | **Window function without `PARTITION BY`** | Entire dataset in one partition; always add `PARTITION BY` on a useful key |
| 3 | **Unsplittable file type** (e.g. Gzip) | Gzip files cannot be split across tasks; use Snappy or LZ4 instead, or re-compress |
| 4 | **`multiLine` option on JSON/CSV** | Forces single-task read; avoid `multiLine=true` on large files when possible |
| 5 | **Schema inference on large file** | Spark reads entire file once to infer schema; provide schema explicitly instead |
| 6 | **`repartition(1)` or `coalesce(1)`** | Explicitly collapses to one partition; remove from production code unless intentional |

## Open questions

- Databricks UDF docs (`/aws/en/udf/`) — not yet captured
- SQL window function reference (`/aws/en/sql/language-manual/sql-ref-window-functions`) — not yet captured

## Related sources

- [[spark-ui-guide]] — parent guide
- [[long-spark-stage]] — Step 2; links here when task count = 1
- [[spark-memory-issues]] — window without `PARTITION BY` also listed as memory cause there
