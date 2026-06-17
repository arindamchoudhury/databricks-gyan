# Spark Memory Issues

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/spark-memory-issues](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/spark-memory-issues)
> **Added:** 2026-06-17
> **Source updated:** 2024-04-15
> **Tags:** spark, spark-ui, debugging, memory, OOM, executors, shuffle, broadcast, UDF, skew, streaming, B2, B16
> **Type:** documentation

## Summary

Sparse index page reached via the [[failing-spark-jobs]] escalation path ("if you've gotten this far, the likeliest explanation is a memory issue"). Gives the canonical OOM error signature, a quick binary test to confirm memory is the issue, and six causes — each linking to a detail page.

## Key points

- Canonical OOM symptom: `ExecutorLostFailure … Remote RPC client disassociated`
- Confirm it's memory: double memory-per-core; if it takes longer to fail (or stops failing), memory is the cause.
- **It's the ratio of cores to memory that matters**, not absolute memory alone.
- Six root causes: too few shuffle partitions, large broadcast, UDFs, window without `PARTITION BY`, skew, streaming state.

## Notes

### Confirming it's a memory issue

The error that signals memory exhaustion:

```
SparkException: Job aborted due to stage failure: Task 3 in stage 0.0 failed 4 times,
most recent failure: Lost task 3.3 in stage 0.0 (TID 30) (10.139.64.114 executor 4):
ExecutorLostFailure (executor 4 exited caused by one of the running tasks)
Reason: Remote RPC client disassociated.
```

**Diagnostic test:** double the memory per core (e.g. switch to a memory-optimized instance type or halve the number of cores on the same node).

> "It's the ratio of cores to memory that matters here. If it takes longer to fail with the extra memory or doesn't fail at all, that's a good sign that you're on the right track."

### Six root causes

| # | Cause | Detail |
|---|---|---|
| 1 | **Too few shuffle partitions** | Tasks processing too much data each; increase partitions or use `spark.sql.shuffle.partitions=auto` → see [[optimize-data-workloads-guide]] spill section |
| 2 | **Large broadcast** | Broadcast table exceeds executor memory; lower `autoBroadcastJoinThreshold` or switch to sort-merge join → see [[optimize-data-workloads-guide]] broadcast section |
| 3 | **UDFs** | UDF loads full partition into Python/JVM memory; `repartition()` before UDF to reduce partition size → see Databricks UDF docs |
| 4 | **Window function without `PARTITION BY`** | Unbounded window = entire dataset in one task's memory; always add `PARTITION BY` → see SQL window function docs |
| 5 | **Skew** | Hot partition overwhelms one executor; partial salting → see [[optimize-data-workloads-guide]] skew section |
| 6 | **Streaming State** | Stateful streaming accumulates unbounded state in memory; use `flatMapGroupsWithState` watermarking or state store tuning → see Spark Structured Streaming docs |

## Open questions

- Databricks UDF docs (`/aws/en/udf/`) — not yet captured
- SQL window function reference (`/aws/en/sql/language-manual/sql-ref-window-functions`) — not yet captured

## Related sources

- [[failing-spark-jobs]] — escalation source; this page is the terminal step for executor failures
- [[spark-ui-guide]] — parent guide
- [[optimize-data-workloads-guide]] — detail for causes 1, 2, 5 (spill, broadcast, skew)
