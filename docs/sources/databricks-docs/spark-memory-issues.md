# Spark Memory Issues

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/spark-memory-issues](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/spark-memory-issues)
> **Added:** 2026-06-17
> **Source updated:** 2024-04-15
> **Tags:** spark, spark-ui, debugging, memory, OOM, executors, shuffle, broadcast, UDF, skew, streaming, B2, B16
> **Type:** documentation

An index page reached via the [[failing-spark-jobs]] escalation path ("if you've gotten this far, the likeliest explanation is a memory issue"). It gives the canonical OOM signature, a quick test to confirm memory is the cause, and six root causes.

## Confirming it's a memory issue

```
SparkException: Job aborted due to stage failure: Task 3 in stage 0.0 failed 4 times,
most recent failure: Lost task 3.3 in stage 0.0 (TID 30) (10.139.64.114 executor 4):
ExecutorLostFailure (executor 4 exited caused by one of the running tasks)
Reason: Remote RPC client disassociated.
```

**Diagnostic test:** double the memory per core (switch to a memory-optimized instance type, or halve the cores on the same node).

> "It's the ratio of cores to memory that matters here. If it takes longer to fail with the extra memory or doesn't fail at all, that's a good sign that you're on the right track."

## Six root causes

| # | Cause | Detail |
|---|---|---|
| 1 | **Too few shuffle partitions** | Tasks processing too much each; increase partitions or `spark.sql.shuffle.partitions=auto` → [[optimize-data-workloads-guide]] (spill) |
| 2 | **Large broadcast** | Broadcast table exceeds executor memory; lower `autoBroadcastJoinThreshold` or use sort-merge → [[optimize-data-workloads-guide]] (broadcast) |
| 3 | **UDFs** | UDF loads a full partition into Python/JVM memory; `repartition()` before the UDF |
| 4 | **Window function without `PARTITION BY`** | Unbounded window = whole dataset in one task's memory; always add `PARTITION BY` |
| 5 | **Skew** | Hot partition overwhelms one executor; partial salting → [[optimize-data-workloads-guide]] (skew) |
| 6 | **Streaming State** | Stateful streaming accumulates unbounded state; use watermarking / state-store tuning |

Related: [[failing-spark-jobs]], [[spark-ui-guide]], [[optimize-data-workloads-guide]], [[one-spark-task]].
