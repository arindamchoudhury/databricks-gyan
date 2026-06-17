# Determine if Longest Stage is I/O Bound

> **Source:** [docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-io](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-io)
> **Added:** 2026-06-17
> **Source updated:** (not shown on page)
> **Tags:** spark, spark-ui, performance, debugging, I/O, shuffle, delta-cache, photon, liquid-clustering, deletion-vectors, B2, B16
> **Type:** documentation

## Summary

Step 4 of the Spark UI diagnostic series. Using the I/O numbers noted in Step 2, calculate whether the stage is I/O bound using a per-core throughput formula (~3 MB/s per core). Then follow the branch for whichever column (Input, Output, Shuffle) shows high I/O — or proceed to Step 5 if none are high.

## Key points

- I/O bound formula: `max_IO_bytes ÷ worker_cores ÷ duration_seconds ≈ 3 MB/s` → I/O bound.
- High input → reading too much → Delta, liquid clustering, Photon, selectivity, Delta cache, DFP.
- High output → writing too much → check rewriting patterns, merges, deletion vectors, Photon.
- High shuffle → `spark.sql.shuffle.partitions=auto`.
- No high I/O in any column → dig deeper → Step 5 (`slow-spark-stage-low-io`).

## Notes

### Is the stage I/O bound?

Use the Input/Output/Shuffle Read/Shuffle Write values from Step 2.

[![Stage I/O columns](assets/spark-ui-guide/08-long-stage-io.jpeg)](assets/spark-ui-guide/08-long-stage-io.jpeg)
*The four I/O columns from the stage list — take the highest value across all four.*

**Formula** (verbatim):

> "How much data needs to be in an I/O column to be considered high? To figure this out, first start with the highest number in any of the given columns. Then consider the total number of CPU cores you have across all our workers. Generally each core can read and write about 3 MBs per second. Divide your biggest I/O column by the number of cluster worker cores, then divide that by duration seconds. If the result is around 3 MB, then you're probably I/O bound. That would be high I/O."

```
max_IO_column_bytes ÷ worker_core_count ÷ duration_seconds ≈ 3 MB/s → I/O bound
```

### High input

> "If you see a lot of input into your stage, that means you're spending a lot of time reading data."

Remediation options (in rough priority order):

| Fix | Why |
|---|---|
| Use Delta | Columnar, indexed, Z-order, data skipping |
| Liquid clustering | Better multi-dimensional data skipping → `/aws/en/tables/clustering` |
| Photon | Faster reads on wide tables |
| More selective predicates | Push filters earlier to reduce scanned data |
| Reconsider data layout | Re-Z-order or re-cluster on filter columns |
| Delta cache | SSD-local cache for repeated reads of same data |
| Dynamic File Pruning (DFP) | Prunes files at join time using runtime filters |
| Increase cluster / use serverless | More cores = more parallel I/O |

### High output

> "If you see a lot of output from your stage, that means you're spending a lot of time writing data."

| Fix | Why |
|---|---|
| Check for excessive rewriting | See `spark-rewriting-data` guide (not yet captured) |
| Optimize merges | Smaller target files (16–64 MB), low-shuffle merge |
| Deletion vectors | Mark deletes without rewriting files → `/aws/en/tables/features/deletion-vectors` |
| Enable Photon | Faster write path |
| Increase cluster / use serverless | More parallel write bandwidth |

### High shuffle

```
spark.sql.shuffle.partitions=auto
```

Lets Spark calculate optimal partition count automatically via AQE. See [[optimize-data-workloads-guide]] for manual tuning formula.

### No high I/O

> "If you don't see high I/O in any of the columns, then you need to dig deeper."

→ Proceed to Step 5: [[slow-spark-stage-low-io]] (`/aws/en/optimizations/spark-ui-guide/slow-spark-stage-low-io`).

## Open questions

- `spark-rewriting-data` — not yet captured (`/aws/en/optimizations/spark-ui-guide/spark-rewriting-data`)

## Related sources

- [[spark-ui-guide]] — parent guide; this is Step 4 of 5
- [[long-spark-stage-page]] — Step 3 (skew/spill); leads here via "Associated Job Ids"
- [[slow-spark-stage-low-io]] — Step 5 (other causes); follows from "no high I/O"
- [[optimize-data-workloads-guide]] — shuffle partition formula, broadcast config, Delta cache vs Spark cache
