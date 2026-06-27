# Look for Skew or Spill

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-page](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-page)
> **Added:** 2026-06-17
> **Source updated:** 2024-04-19
> **Tags:** spark, spark-ui, performance, debugging, skew, spill, memory, shuffle, B2, B16
> **Type:** documentation

Step 3 of the Spark UI diagnostic series. After opening the stage detail page (from Step 2), check two conditions in order — **spill first, then skew**. If neither is present, navigate back to the job via "Associated Job Ids" and proceed to the I/O-bound check (Step 4).

## Check 1 — Spill

Spill = Spark runs low on memory and moves data from RAM to disk (expensive; most common during shuffle stages). Spill statistics appear at the top of the stage page when spill occurred — **no stats = no spill**.

[![Spill statistics](assets/long-spark-stage-page/01.png)](assets/long-spark-stage-page/01.png)

If spill is present, see the spill section of [[optimize-data-workloads-guide]].

## Check 2 — Skew

Skew = one or a few tasks take much longer than the rest → poor cluster utilisation. Go to **Summary Metrics** on the stage detail page and compare **Max duration** vs the **75th percentile**.

[![Skew statistics — Summary Metrics](assets/long-spark-stage-page/02.png)](assets/long-spark-stage-page/02.png)

**Threshold:** `Max duration > 1.5× 75th-percentile` → probable skew (equal Max and P75 → no skew). If skewed, see the skew/salting section of [[optimize-data-workloads-guide]].

## No skew, no spill — navigate to Step 4

Go back to the job page, scroll to top, and click **Associated Job Ids** → proceed to Step 4 ([[long-spark-stage-io]]).

[![Associated Job Ids link](assets/long-spark-stage-page/03.png)](assets/long-spark-stage-page/03.png)

Related: [[spark-ui-guide]], [[long-spark-stage]], [[long-spark-stage-io]], [[optimize-data-workloads-guide]].
