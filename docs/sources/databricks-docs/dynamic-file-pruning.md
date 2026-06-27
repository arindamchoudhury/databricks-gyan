# Dynamic file pruning

> **Source:** [docs.databricks.com/aws/en/optimizations/dynamic-file-pruning](https://docs.databricks.com/aws/en/optimizations/dynamic-file-pruning)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** optimization, performance, dynamic-file-pruning, dfp, delta, join, photon, data-skipping, liquid-clustering, A1
> **Type:** documentation

Dynamic file pruning (DFP) improves query performance on Delta tables by **skipping data files at runtime** based on filter/`WHERE` predicates — including filters propagated from the small side of a join into the scan of the large side. It's triggered by the optimizer for queries with filters and is **default-on**. Most efficient for non-partitioned tables or joins on non-partitioned columns; benefit correlates with how well data is clustered.

> "Dynamic file pruning in MERGE, UPDATE, and DELETE statements requires Photon-enabled compute. For SELECT statements, Photon provides broader and more reliable dynamic file pruning."

## Configuration thresholds

| Config | Default | Meaning |
|---|---|---|
| `spark.databricks.optimizer.dynamicFilePruning` | `true` | Master flag; `false` disables DFP entirely |
| `spark.databricks.optimizer.deltaTableSizeThreshold` | 10 GB | Min size of probe-side Delta table to trigger DFP |
| `spark.databricks.optimizer.deltaTableFilesThreshold` | 10 | Min number of files on probe side to trigger DFP |

Rationale: if the probe side is small (few bytes/files), pushing down filters isn't worthwhile — just scan the whole table. Find a table's size/file count with `DESCRIBE DETAIL table_name` (`sizeInBytes`, `numFiles`).

## When it shines

> "Dynamic file pruning is especially efficient for non-partitioned tables, or for joins on non-partitioned columns. The performance effect of dynamic file pruning is often correlated to the clustering of data, so consider using liquid clustering to maximize the benefit."

Canonical case: a star-schema **fact × dimension** join — a selective filter on the small dimension prunes files from the large fact scan.

Related: [[liquid-clustering]], [[photon]], [[optimization-recommendations]].
