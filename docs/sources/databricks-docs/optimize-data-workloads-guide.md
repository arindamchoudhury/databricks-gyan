# Comprehensive Guide to Optimize Databricks, Spark and Delta Lake Workloads

> **Source:** [databricks.com/discover/pages/optimize-data-workloads-guide](https://www.databricks.com/discover/pages/optimize-data-workloads-guide)
> **Added:** 2026-06-17
> **Source updated:** (no date on page)
> **Tags:** spark, performance, optimization, delta-lake, shuffle, skew, spill, merge, vacuum, caching, photon, B2, B5, B12, B16, B17
> **Type:** documentation

An end-to-end practitioner handbook covering data layout, shuffle control, spill and skew diagnosis, data skipping, caching, Delta Merge internals, and cluster configuration — with specific thresholds and configs throughout. All optimizations assume **Delta** as the table format, and the guide frames cost as a **nonfunctional requirement** to design for from project inception, not an afterthought.

## Data layout

**File sizing:**

| Target | Size |
|---|---|
| Optimize Write (per partition) | 128 MB |
| Auto Compact target | 128 MB |
| Post-OPTIMIZE max | up to 1 GB (configurable) |
| Merge-heavy tables | 16–64 MB (smaller = less rewrite per merge) |
| Recommended range | 16 MB – 1 GB |

**Z-order:** high-cardinality columns only (`customer_id`, not `year`), **max 4 columns**, run `OPTIMIZE` on a separate job cluster (not inline).

**Partitioning:** don't partition tables under 1 TB; partition only if each partition holds ≥ 1 GB; use low-cardinality keys (`year`, `date`).

## Data shuffling

Spark auto-broadcasts tables < 10 MB. Raising the threshold (safe up to ~200 MB if the driver has 32 GB+ RAM; hard limits: Spark broadcast 8 GB/table, driver collect 1 GB):

```python
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 200 * 1024 * 1024)
```

Shuffle hash join for medium tables: `spark.sql.join.preferSortMergeJoin=false`. Cost-based optimizer: `ANALYZE TABLE … COMPUTE STATISTICS` (daily or after >10% mutation) with `spark.sql.cbo.enabled=true` and `spark.sql.cbo.joinReorder.enabled=true`.

## Data spilling

Enable both AQE auto-tuners: `spark.sql.adaptive.coalescePartitions.enabled=true` and `spark.sql.adaptive.skewJoin.enabled=true`. For highly compressed tables start at 16 MB (`spark.sql.adaptive.preshufflePartitionSizeInBytes=16777216`), reduce to 8 MB if spill persists.

[![Spill diagnosis in the Spark UI](assets/optimize-data-workloads-guide/08.png)](assets/optimize-data-workloads-guide/08.png)

Manual shuffle-partition tuning — target ~128–200 MB of shuffle data per task:

```
num_partitions = total_shuffled_bytes / (128MB to 200MB)   # formula
num_partitions = 2× to 3× total_worker_cores               # conservative baseline
```

## Data skewness

**Identify:** tasks summary shows a large gap between min and max shuffle read size; or most tasks finish but 1–2 hang indefinitely.

[![Skew visible in the tasks summary](assets/optimize-data-workloads-guide/13.png)](assets/optimize-data-workloads-guide/13.png)

**Remediate with partial salting** (a last resort, applied only to known-skewed values, not all data): identify the skewed key → append a random suffix `0..N` to split the hot partition → join/aggregate the salted partitions, then union/re-aggregate to remove the salt.

## Data explosion

`explode()` converts array/map columns to rows (the **Generate** node in the SQL DAG), and an unconstrained join can produce GBs per task (watch "rows output" on join nodes).

[![Row explosion in the SQL DAG](assets/optimize-data-workloads-guide/17.png)](assets/optimize-data-workloads-guide/17.png)

```python
spark.conf.set("spark.sql.files.maxPartitionBytes", 16 * 1024 * 1024)  # reduce input partition size
df.repartition(n)                                                       # or repartition before the join
spark.conf.set("spark.sql.shuffle.partitions", n)                       # or more shuffle partitions for join output
```

## Data skipping and pruning

Delta collects min/max stats on the **first 32 columns** of each Parquet file automatically. Apply filters **immediately after the table read** (predicate pushdown), filter on partition columns (partition pruning), `SELECT` only needed columns (column pruning); Dynamic Partition Pruning and Dynamic File Pruning are on by default since Spark 3.0.

## Caching

**Delta cache** (preferred) copies remote files to node-local SSD, transparently, requiring Storage Optimized instances. **Spark cache** only helps when the same DataFrame is used in 2+ actions and is evicted on restart. Databricks recommends **Delta cache over Spark cache**.

## Delta Merge internals

Merge runs in two phases: (1) an **inner join** (source ↔ target on the `ON` clause) produces the list of target files with matching rows; (2) the **write phase** either appends (no matches — fast) or does a **full outer join** on the matching target files + source and rewrites them. A loose `ON` clause → many matching files → lots of rewrite; after many merges, Z-order degrades (re-`OPTIMIZE` periodically).

| Technique | Effect |
|---|---|
| Smaller target files (16–64 MB) | Reduces bytes rewritten per merge |
| Partition filter in `ON` clause | Limits files scanned in phase 1 |
| Z-order column filter | Further limits file candidates |
| Broadcast source (≤ 200 MB) | Avoids shuffle in phase 1 |
| Low shuffle merge | Rewrites only changed rows; keeps unmodified rows in place |

## Data purging — VACUUM

```sql
VACUUM table_name RETAIN 168 HOURS  -- 7-day minimum
```

Default retention 7 days (`delta.logRetentionDuration` 30 days for the transaction log). **Never** set retention below 7 days (concurrent readers may reference old snapshots), and run VACUUM as a **separate job**, not inline with ETL.

## Cluster configuration

[![Cluster configuration guidance](assets/optimize-data-workloads-guide/24.png)](assets/optimize-data-workloads-guide/24.png)

| Instance type | Use for |
|---|---|
| Memory Optimized | ML workloads; heavy shuffle and spill |
| Compute Optimized | OPTIMIZE and Z-order jobs |
| Storage Optimized | Delta caching workloads |

Sizing: small 2–4 workers, medium/large 8–10, never single-worker for production. Autoscaling: enable on interactive clusters (min 1); for production set min to the compute floor; **never use autoscaling for Spark Structured Streaming** (use Lakeflow declarative pipelines' enhanced autoscaling instead). Enable **Photon** for MERGE-heavy ETL, large scans, joins, and aggregations; enable **auto-termination** on all all-purpose clusters (default 120 min idle).

Related: [[spark-ui-guide]], [[photon]], [[liquid-clustering]], [[predictive-optimization]], [[classic-compute-configure]], [[compute-pools]].
