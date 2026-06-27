# Diagnose cost and performance issues using the Spark UI

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide)
> **Added:** 2026-06-17
> **Source updated:** 2024-04-19
> **Tags:** spark, spark-ui, performance, optimization, debugging, skew, spill, stages, tasks, B2, B16
> **Type:** documentation

A practical **five-step** diagnostic workflow for using the Spark UI to find performance and cost issues — it teaches *how to investigate* rather than what each feature does: start at the Jobs Timeline, drill into the longest job, then the longest stage, check for spill and skew, quantify I/O, and finally look for structural causes (small files, UDFs, bad joins).

## Step 1 — Jobs Timeline

Open via **Jobs → Event Timeline**. Classify what you see before drilling in:

[![Jobs Timeline](assets/spark-ui-guide/01-jobs-timeline.png)](assets/spark-ui-guide/01-jobs-timeline.png)

- **Failing jobs or executors** — red status → [[failing-spark-jobs]].

[![Failing jobs in timeline](assets/spark-ui-guide/02-failing-jobs.png)](assets/spark-ui-guide/02-failing-jobs.png)

- **Gaps ≥ 1 minute mid-pipeline** — driver blocked or resource wait (short gaps are normal).

[![Job gaps](assets/spark-ui-guide/03-job-gaps.png)](assets/spark-ui-guide/03-job-gaps.png)

- **One or few long jobs dominating** — compute bottleneck; click the longest.

[![Long jobs](assets/spark-ui-guide/04-long-jobs.png)](assets/spark-ui-guide/04-long-jobs.png)

- **Many tiny jobs** — over-orchestration or small-file reads.

[![Small jobs](assets/spark-ui-guide/05-small-jobs.png)](assets/spark-ui-guide/05-small-jobs.png)

- **Default case** — sort the jobs table by Duration, click the worst offender.

[![Find the long job](assets/spark-ui-guide/06-find-long-job.png)](assets/spark-ui-guide/06-find-long-job.png)

## Step 2 — Longest stage

Scroll to the stage list at the bottom of the job page; sort by **Duration**.

[![Stage list by duration](assets/spark-ui-guide/07-long-stage.png)](assets/spark-ui-guide/07-long-stage.png)

Note the four I/O metrics — Input (storage reads), Output (storage writes), Shuffle Read, Shuffle Write.

[![Stage I/O columns](assets/spark-ui-guide/08-long-stage-io.jpeg)](assets/spark-ui-guide/08-long-stage-io.jpeg)

> ⚠️ Note these numbers — you'll need them in Step 4.

[![Task count in stage detail](assets/spark-ui-guide/09-long-stage-tasks.jpeg)](assets/spark-ui-guide/09-long-stage-tasks.jpeg)

Task count branch: **1 task** → [[one-spark-task]]; **>1 task** → click the stage description to open stage detail.

[![Stage description link](assets/spark-ui-guide/10-long-stage-description.png)](assets/spark-ui-guide/10-long-stage-description.png)

## Step 3 — Skew or spill

**Spill** (low memory → data moves RAM→disk; most common in shuffles) — if spill statistics appear in the stage detail, this stage has spill.

[![Spill statistics](assets/spark-ui-guide/11-spill-stats.png)](assets/spark-ui-guide/11-spill-stats.png)

**Skew** (a few tasks take far longer than the rest) — check **Summary Metrics**: `Max duration > 1.5× 75th-percentile` → probable skew.

[![Skew statistics](assets/spark-ui-guide/12-skew-stats.png)](assets/spark-ui-guide/12-skew-stats.png)

No skew, no spill → go back to the job page and click **Associated Job Ids** → Step 4.

[![Associated Job Ids](assets/spark-ui-guide/13-stage-to-job.png)](assets/spark-ui-guide/13-stage-to-job.png)

## Step 4 — Is the stage I/O bound?

```
max_IO_column_bytes ÷ worker_core_count ÷ duration_seconds ≈ 3 MB/s → I/O bound
```

Each core reads/writes ~3 MB/s; if your per-core rate approaches that, you're I/O bound. Then:

- **High input** (reading too much): use Delta; liquid clustering; Photon; more selective predicates; Delta cache; dynamic file pruning; bigger cluster / serverless.
- **High output** (writing too much): check excessive rewriting (optimize merges / deletion vectors); enable Photon; bigger cluster / serverless.
- **High shuffle:** `SET spark.sql.shuffle.partitions = auto;`
- **No high I/O** → Step 5.

## Step 5 — Other causes (low I/O, slow stage)

Navigate from stage detail to the **SQL DAG**; times are **cumulative** (total across tasks, not wall-clock).

[![Stage to SQL link](assets/spark-ui-guide/14-stage-to-sql.png)](assets/spark-ui-guide/14-stage-to-sql.png)
[![SQL DAG](assets/spark-ui-guide/15-sql-dag.png)](assets/spark-ui-guide/15-sql-dag.png)
[![Slow node in DAG](assets/spark-ui-guide/16-slow-stage-in-dag.png)](assets/spark-ui-guide/16-slow-stage-in-dag.png)

**1. Reading many small files** — tens of thousands of files / files < 8 MB; root cause over-partitioning. Fix: `OPTIMIZE`, predictive optimization, fewer/lower-cardinality partition keys.

[![Many files read](assets/spark-ui-guide/18-many-files-read.png)](assets/spark-ui-guide/18-many-files-read.png)

**2. Writing many small files** — same root cause. Fix: predictive optimization, optimized writes, reconsider layout.

[![Many files write](assets/spark-ui-guide/19-many-files-write.png)](assets/spark-ui-guide/19-many-files-write.png)
[![Slow write node](assets/spark-ui-guide/17-slow-write-node.png)](assets/spark-ui-guide/17-slow-write-node.png)

**3. Slow UDFs** — `repartition(num_cores)` before the UDF if task count < cores, or rewrite with native functions (eliminates serialization overhead).

**4. Cartesian join** — `CartesianProduct` / `BroadcastNestedLoopJoin` (O(N×M)); verify intent, seek an equi-join.

**5. Exploding join / `explode()`** — few rows in, magnitudes more out; watch for accidental cross-joins or unconstrained `explode()`.

[![Exploding join fan-out in DAG](assets/spark-ui-guide/20-exploding-join.png)](assets/spark-ui-guide/20-exploding-join.png)

Related: [[long-spark-stage]], [[long-spark-stage-page]], [[long-spark-stage-io]], [[slow-spark-stage-low-io]], [[failing-spark-jobs]], [[one-spark-task]], [[photon]], [[optimize-data-workloads-guide]].
