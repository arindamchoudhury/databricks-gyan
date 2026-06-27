# Look for Other Causes of Slow Stage Runtime

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/slow-spark-stage-low-io](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/slow-spark-stage-low-io)
> **Added:** 2026-06-17
> **Source updated:** 2026-03-06
> **Tags:** spark, spark-ui, performance, debugging, small-files, UDF, cartesian-join, explode, DAG, B2, B16
> **Type:** documentation

Step 5 of the Spark UI diagnostic series — reached when Step 4 finds no high I/O. Read the SQL DAG to find where time accumulates, then diagnose one of five structural causes: small files on read, small files on write, slow UDFs, cartesian joins, or exploding joins / `explode()`.

## Navigate to the SQL DAG

From the job page, click **Associated SQL Query** at the top.

[![Stage to SQL link](assets/slow-spark-stage-low-io/01.png)](assets/slow-spark-stage-low-io/01.png)
[![SQL DAG](assets/slow-spark-stage-low-io/02.png)](assets/slow-spark-stage-low-io/02.png)

> "these times are cumulative, so it's the total time spent on all the tasks, not the clock time."

Identify the node consuming the most time — that's the cause to diagnose (some nodes show timing directly; others need expanding).

[![Slow stage node in the DAG](assets/slow-spark-stage-low-io/03.png)](assets/slow-spark-stage-low-io/03.png)

## Cause 1 — Reading many small files

> "If you're reading tens of thousands of files or more, you may have a small file problem. Your files should be no less than 8MB."

Most often caused by partitioning on too many columns or a high-cardinality column. Check the **scan operator** for file counts.

[![Scan operator with high file count](assets/slow-spark-stage-low-io/05.png)](assets/slow-spark-stage-low-io/05.png)

Fixes: run `OPTIMIZE` to compact; enable **predictive optimization**; reconsider layout (fewer/lower-cardinality partition keys).

## Cause 2 — Writing many small files

Same root cause (over-partitioning / high-cardinality partition columns); check the write operator.

[![Write operator with excessive file count](assets/slow-spark-stage-low-io/06.png)](assets/slow-spark-stage-low-io/06.png)
[![A slow write node in the DAG](assets/slow-spark-stage-low-io/04.png)](assets/slow-spark-stage-low-io/04.png)

Fixes: enable **predictive optimization**; enable **optimized writes** (merges small shuffle outputs before writing); reconsider layout.

## Cause 3 — Slow UDFs

UDFs appear as named DAG nodes. **Diagnose:** comment out the UDF and rerun — if the pipeline speeds up, the UDF is the cause.

> "If the UDF is indeed where the time is being spent, your best bet is to rewrite the UDF using native functions."

Fix 1: rewrite with native functions (eliminates serialization overhead). Fix 2: `repartition(num_cores)` before the UDF when task count < core count:

```python
df.repartition(num_cores).withColumn('new_col', udf_fn(...))
```

> "Each task may have to load all the data in its partition into memory… Repartition also can resolve this issue by making each task smaller."

## Cause 4 — Cartesian join

Signal: a `CartesianProduct` or `BroadcastNestedLoopJoin` node. "these joins are very expensive" — verify intent; redesign to an equi-join if possible.

## Cause 5 — Exploding join or `explode()`

> "If you see a few rows going into a node and magnitudes more coming out, you may be suffering from an exploding join or explode()."

[![Row-count fan-out in the DAG](assets/slow-spark-stage-low-io/07.png)](assets/slow-spark-stage-low-io/07.png)

Verify the fan-out is intentional; add filters before the explode/join. See the data-explosion section of [[optimize-data-workloads-guide]] (`maxPartitionBytes`, `repartition()`).

Related: [[spark-ui-guide]], [[long-spark-stage-io]], [[optimize-data-workloads-guide]], [[predictive-optimization]].
