# Determine if Longest Stage is I/O Bound

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-io](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-io)
> **Added:** 2026-06-17
> **Source updated:** 2026-06-11
> **Tags:** spark, spark-ui, performance, debugging, I/O, shuffle, delta-cache, photon, liquid-clustering, deletion-vectors, B2, B16
> **Type:** documentation

Step 4 of the Spark UI diagnostic series. Using the I/O numbers noted in Step 2, calculate whether the stage is I/O bound (~3 MB/s per core), then follow the branch for whichever column (Input, Output, Shuffle) shows high I/O — or proceed to Step 5 if none are.

## Is the stage I/O bound?

Use the Input / Output / Shuffle Read / Shuffle Write values from Step 2.

[![The four I/O columns from the stage list](assets/long-spark-stage-io/01.jpeg)](assets/long-spark-stage-io/01.jpeg)
*Take the highest value across all four columns.*

> "…each core can read and write about 3 MBs per second. Divide your biggest I/O column by the number of cluster worker cores, then divide that by duration seconds. If the result is around 3 MB, then you're probably I/O bound."

```
max_IO_column_bytes ÷ worker_core_count ÷ duration_seconds ≈ 3 MB/s → I/O bound
```

## High input

> "If you see a lot of input into your stage, that means you're spending a lot of time reading data."

Remediation (rough priority): use **Delta**; **liquid clustering** (better multi-dimensional skipping); **Photon**; more selective predicates; reconsider data layout (re-cluster on filter columns); **Delta cache** (repeated reads); **dynamic file pruning**; bigger cluster / serverless.

## High output

> "If you see a lot of output from your stage, that means you're spending a lot of time writing data."

Check for excessive rewriting ([[spark-rewriting-data]]); optimize merges (smaller target files 16–64 MB, low-shuffle merge); **deletion vectors** (mark deletes without rewriting files); enable Photon; bigger cluster / serverless.

## High shuffle

```
spark.sql.shuffle.partitions=auto
```

Lets Spark calculate the optimal partition count via AQE; see [[optimize-data-workloads-guide]] for the manual formula.

## No high I/O

> "If you don't see high I/O in any of the columns, then you need to dig deeper."

→ Proceed to Step 5 ([[slow-spark-stage-low-io]]).

Related: [[spark-ui-guide]], [[long-spark-stage-page]], [[slow-spark-stage-low-io]], [[spark-rewriting-data]], [[optimize-data-workloads-guide]].
