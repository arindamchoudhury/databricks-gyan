# Use liquid clustering for tables

> **Source:** [docs.databricks.com/aws/en/tables/clustering](https://docs.databricks.com/aws/en/tables/clustering)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-18
> **Tags:** tables, delta, iceberg, liquid-clustering, cluster-by, optimize, zorder, partitioning, predictive-optimization, automatic-clustering, data-skipping, A2, I5
> **Type:** documentation

## Summary
Liquid clustering is the data-layout strategy that **replaces both partitioning and ZORDER**. You set clustering keys with `CLUSTER BY`; the engine organizes data for data skipping, and unlike partitioning you can **redefine keys without rewriting existing data**. GA for Delta on DBR 15.4 LTS+, Public Preview for Iceberg on DBR 16.4 LTS+. Databricks recommends it for **all new tables** (incl. streaming tables + materialized views), and recommends `CLUSTER BY AUTO` (automatic key selection via predictive optimization) over hand-picking keys.

## Key points

- `CLUSTER BY` replaces `PARTITIONED BY` / `ZORDER` — they are mutually exclusive.
- Keys are mutable: `ALTER TABLE … CLUSTER BY (...)` any time; existing data not rewritten until `OPTIMIZE`.
- Up to **4 clustering keys**; must be columns with statistics collected (default first 32 cols).
- **Automatic** liquid clustering: `CLUSTER BY AUTO` (DBR 15.4 LTS+, UC managed tables) — predictive optimization picks keys from query history, adapts over time, cost-aware.
- Triggering: predictive optimization runs `OPTIMIZE` automatically on managed tables. Manually: `OPTIMIZE table` (incremental) or `OPTIMIZE table FULL` (force full recluster).
- Convert partitioned table (DBR 18.1+): `ALTER TABLE … REPLACE PARTITIONED BY WITH CLUSTER BY [(...) | AUTO]`.
- Delta tables with LC use writer v7 / reader v3 — **can't downgrade protocol**; old clients can't read.
- Clustering on write only fires above per-key size thresholds (lower for UC managed tables).

## Notes

### When to use it

Recommended for **all new tables**. Particularly benefits:

- Queries filtering on **high-cardinality** columns.
- Tables with heavy **data skew**.
- Fast-growing tables needing maintenance/tuning effort.
- Tables with **concurrent write** requirements.
- Tables with varied / changing access patterns.
- Tables where a partition key returns too many or too few partitions.

> **Version support:** GA for Delta Lake on **DBR 15.4 LTS+**; Public Preview for Apache Iceberg on **DBR 16.4 LTS+**. Managed Iceberg **v3** tables also get deletion vectors, row tracking, row-level concurrency, and automatic LC — requires **DBR 18.0+**.

### Enable on new tables

`CLUSTER BY` goes in the create statement. DBR 14.3 LTS+ also supports DataFrame / DeltaTable APIs (Python/Scala).

```sql
-- empty table
CREATE TABLE table1 (col0 INT, col1 STRING) CLUSTER BY (col0);

-- from existing data: CLUSTER BY after table name, NOT in SELECT
CREATE TABLE table2 CLUSTER BY (col0)
AS SELECT * FROM table1;

-- copy structure incl. clustering config
CREATE TABLE table3 LIKE table1;
```

Python (DeltaTable / DataFrame APIs):

```python
(DeltaTable.create()
  .tableName("table1")
  .addColumn("col0", dataType="INT")
  .addColumn("col1", dataType="STRING")
  .clusterBy("col0")
  .execute())

df.write.clusterBy("col0").saveAsTable("table2")
df.writeTo("table1").using("delta").clusterBy("col0").create()  # DataFrameWriterV2, DBR 14.2+
```

> **DataFrame API caveat:** clustering keys can only be set at **table creation or overwrite** mode (e.g. `CREATE OR REPLACE`). You **cannot** change keys in **append** mode — use SQL `ALTER TABLE` to change keys separately from writes.

DBR 16.4 LTS+: can create LC tables via Structured Streaming writes:

```python
(spark.readStream.table("source_table")
  .writeStream
  .clusterBy("column_name")
  .option("checkpointLocation", checkpointPath)
  .toTable("target_table"))
```

> **Protocol warning:** Delta LC tables use **writer v7 / reader v3**. Clients lacking these protocols can't read them; you can't downgrade. To override feature enablement (e.g. keep deletion vectors off), see "Override default feature enablement" below.

### Enable on existing tables

```sql
ALTER TABLE <table_name> CLUSTER BY (<clustering_columns>)
```

- Managed Iceberg **v2**: must explicitly turn off deletion vectors + row tracking first. **v3**: not required (both supported).
- Default does **not** cluster previously written data. Force with `OPTIMIZE FULL` / `OPTIMIZE FULL WHERE <predicate>`.

### Convert a partitioned table → LC (DBR 18.1+)

```sql
ALTER TABLE <table_name>
REPLACE PARTITIONED BY WITH CLUSTER BY [( <clustering_columns> ) | AUTO]
```

`CLUSTER BY` options:

- `( columns )` — new keys. Keep them **similar to original partition columns**; very different cols trigger a large recluster on first `OPTIMIZE`.
- `AUTO` — uses current partition cols as initial keys, lets predictive optimization adapt. **UC managed tables only.**
- no options — uses current partition cols as new keys.

Minimizes reader/writer downtime; supports external + managed tables. After conversion, reads supported on **DBR 13.3 LTS+**. (Managed Iceberg: conversion unnecessary — partition defs already act as LC keys; running the command errors.)

Examples:

```sql
ALTER TABLE t1 REPLACE PARTITIONED BY WITH CLUSTER BY (day, id);
OPTIMIZE t1;   -- required to benefit from new keys

ALTER TABLE t2 REPLACE PARTITIONED BY WITH CLUSTER BY AUTO;
ALTER TABLE t3 REPLACE PARTITIONED BY WITH CLUSTER BY;   -- keep partition cols as keys
```

**Concurrent reads/writes during conversion:** batch reads = no downtime (any DBR). Batch writes = no downtime on DBR 15.4+; pause on ≤15.3. Streaming reads: with schema tracking + column mapping, restart without losing commits; without, stream raises exception → restart with new checkpoint + start version (commits not lost). Streaming writes: restart without losing commits. DBR 15.4 LTS+ recommended for concurrent workloads.

**Verify / roll back:** `DESCRIBE EXTENDED` shows new keys; `DESCRIBE HISTORY` shows `REORG`, `UPGRADE PROTOCOL`, `REPLACE PARTITIONED BY WITH CLUSTER BY`. Roll back via `RESTORE`:

```sql
ALTER TABLE my_table CLUSTER BY NONE;
ALTER TABLE my_table UNSET TBLPROPERTIES ('delta.liquid.hierarchicalClusteringColumns');
RESTORE TABLE my_table TO VERSION AS OF <version_before_conversion>;
```

**Timestamp partition column** conversion needs extra config or it errors (`unsupported type: timestamp`):

```sql
SET spark.databricks.delta.liquidConversion.statsGeneration.enabled = false;
ALTER TABLE t1 REPLACE PARTITIONED BY WITH CLUSTER BY (timestamp_col, id);
ANALYZE TABLE t1 COMPUTE DELTA STATISTICS;
```

**Conversion limitations:** not supported for streaming tables / MVs created in Lakeflow Spark Declarative Pipelines (update the pipeline to `CLUSTER BY` instead); not supported for tables using Delta Sharing with partition filtering.

### Remove keys

```sql
ALTER TABLE table_name CLUSTER BY NONE;
```

### Choosing clustering keys

- Pick the columns **most frequently used in query filters** — that's what drives data skipping.
- Keys can be in any order. If two columns are highly correlated, include only one.
- **Up to 4 keys.** For small tables (<10 TB), more keys can *degrade* single-column filter performance (4 keys worse than 2); difference becomes negligible as table grows.
- Keys must be columns with statistics (default first 32 columns).
- Databricks recommends `CLUSTER BY AUTO` to let the platform pick.

**Supported key types:** Date, Timestamp, TimestampNTZ (DBR 14.3 LTS+), String, Integer/Long/Short/Byte, Float/Double/Decimal. Struct fields via dot notation (`CLUSTER BY (struct_col.nested.field)`, any depth). **Not** allowed: complex types (Struct/Map/Array) themselves, or Map/Array elements.

**Migrating from partitioning / Z-order** (key recommendation):

| Current technique | Clustering keys to use |
|---|---|
| Hive-style partitioning | Use the partition columns |
| Z-order | Use the `ZORDER BY` columns |
| Partitioning + Z-order | Use both sets |
| Generated column to reduce cardinality (e.g. `date` from timestamp) | Use the original column; drop the generated column |

### Automatic liquid clustering (`CLUSTER BY AUTO`)

DBR 15.4 LTS+ for UC managed **Delta** tables; DBR 18.0+ for managed **Iceberg v3**. Also supported for MVs + streaming tables (incl. Lakeflow pipelines — specify `CLUSTER BY AUTO` in the definition).

How it works (requires **predictive optimization**, runs async):

- Analyzes historical query workload → picks best candidate columns.
- Adapts when query patterns / data distribution change.
- **Cost-aware:** changes keys only when predicted skipping savings outweigh clustering cost.

May **not** select keys when: table too small; already well-clustered (manual keys or natural insertion order); table rarely queried; not on DBR 15.4 LTS+. You can enable it on *any* managed table regardless — heuristics decide if it's worth it.

```sql
CREATE OR REPLACE TABLE table1 (column01 int, column02 string) CLUSTER BY AUTO;
ALTER TABLE table1 CLUSTER BY AUTO;                  -- enable on existing
ALTER TABLE table1 CLUSTER BY (c1, c2);              -- set hint columns…
ALTER TABLE table1 CLUSTER BY AUTO;                  -- …then turn on AUTO
ALTER TABLE table1 CLUSTER BY NONE;                  -- turn off
```

> **CREATE OR REPLACE gotcha:** running `CREATE OR REPLACE table` **without** `CLUSTER BY AUTO` turns off automatic clustering and does **not** preserve clustering columns. Include `CLUSTER BY AUTO` in the replace to keep it.

Check status: `DESCRIBE TABLE` / `SHOW TBLPROPERTIES` → `clusterByAuto = true`, `clusteringColumns` shows current keys.

**Limitation:** not available for managed Iceberg **v2**; supported for Iceberg **v3** on DBR 18.0+.

### Writing to a clustered table

Operations that **cluster on write**: `INSERT INTO`, `CTAS`/`RTAS`, `COPY INTO` from Parquet, `spark.write.mode("append")`.

**Size thresholds** — clustering on write only triggers when the transaction's data exceeds a threshold (lower for UC managed tables):

| # clustering columns | UC managed table | Other Delta table |
|---|---|---|
| 1 | 64 MB | 256 MB |
| 2 | 256 MB | 1 GB |
| 3 | 512 MB | 2 GB |
| 4 | 1 GB | 4 GB |

Because not all ops cluster on write, run `OPTIMIZE` frequently. **Streaming:** set `spark.databricks.delta.liquid.eagerClustering.streaming.enabled = true`; triggers only if ≥1 of last 5 streaming updates exceeds a threshold.

### Triggering clustering

Predictive optimization auto-runs `OPTIMIZE` on enabled tables (disable any scheduled `OPTIMIZE` jobs when using it). Manual:

```sql
OPTIMIZE table_name;          -- incremental; only rewrites data needing clustering
OPTIMIZE table_name FULL;     -- force full recluster (DBR 16.4 LTS+)
OPTIMIZE events FULL WHERE event_date >= '2025-01-01';  -- partial recluster, DBR 18.1+
```

- `OPTIMIZE` is **incremental** — won't rewrite files whose keys already match.
- Run `OPTIMIZE FULL` on first enable or after changing keys. If keys unchanged since last `FULL`, it behaves like incremental `OPTIMIZE`.
- Without predictive optimization, schedule `OPTIMIZE` regularly — every 1–2 h for high-update tables. DBR 17.3 LTS+ recommended for faster `OPTIMIZE` on large tables.

### Reading & managing

Read with any Delta client supporting deletion vectors (Iceberg: via UC Iceberg REST Catalog API, DBR 13.3 LTS+). Data skipping kicks in when filtering on clustering keys.

```sql
DESCRIBE TABLE table_name;      -- see keys
DESCRIBE DETAIL table_name;
ALTER TABLE table_name CLUSTER BY (new_column1, new_column2);  -- change keys (existing data not rewritten)
ALTER TABLE table_name CLUSTER BY NONE;                        -- stop using keys
```

### From an external engine (managed Iceberg)

External Iceberg engines: specify partition columns at create → UC interprets them as clustering keys.

```sql
CREATE OR REPLACE TABLE main.schema.icebergTable PARTITIONED BY c1;       -- OSS Spark
ALTER TABLE main.schema.icebergTable DROP PARTITION FIELD c2;             -- turn off
ALTER TABLE main.schema.icebergTable ADD PARTITION FIELD c2;             -- change keys (partition evolution)
CREATE OR REPLACE TABLE main.schema.icebergTable PARTITIONED BY (bucket(c1, 10));  -- bucket transform dropped, c1 used as key
```

### Override default feature enablement (optional)

Turn off a Delta feature before enabling LC to avoid the protocol upgrade:

| Delta feature | Runtime compat | Property | Effect if off |
|---|---|---|---|
| Deletion vectors | RW DBR 12.2 LTS+ | `'delta.enableDeletionVectors'='false'` | Also disables row-level concurrency → more conflicts; DELETE/MERGE/UPDATE slower |
| Row tracking | Write DBR 13.3 LTS+, read any | `'delta.enableRowTracking'='false'` | Also disables row-level concurrency → more conflicts |
| Checkpoint V2 | RW DBR 13.3 LTS+ | `'delta.checkpointPolicy'='classic'` | No effect on LC behavior |

### Compatibility

LC tables created on DBR 14.3 LTS+ use **checkpoint V2** by default (readable/writable DBR 13.3 LTS+). To support readers on DBR 12.2 LTS–13.2, disable checkpoint V2 and downgrade the protocol.

### Limitations

- DBR ≤15.1: clustering on write doesn't support source queries with filters/joins/aggregations.
- DBR ≤15.4 LTS: can't *create* an LC table via Structured Streaming write (can write to an existing one).
- Managed Iceberg v2: no row-level concurrency (no deletion vectors / row tracking). v3 supports it.

## Quotes worth keeping

> "Unlike traditional partitioning, you can redefine clustering keys without rewriting existing data." (intro)

> "Clustering is not compatible with partitioning or ZORDER." (Enable liquid clustering)

> "Liquid clustering is incremental, meaning that OPTIMIZE only rewrites data as necessary to accommodate data that needs clustering." (How to trigger clustering)

## Open questions

- Iceberg v2 vs v3 capability split is scattered across the page — a single matrix would help; for now: v3 = DBR 18.0+ adds DV / row tracking / row-level concurrency / automatic LC.
- Exact heuristics predictive optimization uses to pick `AUTO` keys aren't published (same gap as [[predictive-optimization]]).

## Related sources

- [[predictive-optimization]] — automatic LC *depends on* predictive optimization for key selection + running `OPTIMIZE`; that note covers the maintenance engine, this one the layout strategy it drives.
- [[ch02-managing-data-with-delta-lake]] — manual `OPTIMIZE`/`VACUUM`/Z-order mechanics LC supersedes.
- [[optimize-data-workloads-guide]] — broader perf-tuning guide; LC is the storage-layout lever it points to.
- [[aqe]] — runtime query optimization; complements LC's write-time data-skipping layout.
- [[managed-tables]] — automatic LC + lower write thresholds are managed-table advantages noted there.
