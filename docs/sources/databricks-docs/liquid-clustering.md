# Use liquid clustering for tables

> **Source:** [docs.databricks.com/aws/en/tables/clustering](https://docs.databricks.com/aws/en/tables/clustering)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-18
> **Tags:** tables, delta, iceberg, liquid-clustering, cluster-by, optimize, zorder, partitioning, predictive-optimization, automatic-clustering, data-skipping, A2, I5
> **Type:** documentation

Liquid clustering is the data-layout strategy that **replaces both partitioning and ZORDER**. You set clustering keys with `CLUSTER BY`; the engine organizes data for data skipping, and — unlike partitioning — you can **redefine keys without rewriting existing data**. GA for Delta on **DBR 15.4 LTS+**, Public Preview for Iceberg on **DBR 16.4 LTS+**. Databricks recommends it for **all new tables** (incl. streaming tables + materialized views), and recommends `CLUSTER BY AUTO` (automatic key selection via predictive optimization) over hand-picking keys.

> "Unlike traditional partitioning, you can redefine clustering keys without rewriting existing data." · "Clustering is not compatible with partitioning or ZORDER."

`CLUSTER BY` and `PARTITIONED BY`/`ZORDER` are mutually exclusive. Up to **4 keys**, on columns with statistics (default first 32 cols). Delta LC tables use **writer v7 / reader v3** — can't downgrade the protocol, and old clients can't read them.

## When to use it

Recommended for **all new tables**, particularly: queries filtering on **high-cardinality** columns; tables with heavy **data skew**; fast-growing tables; tables with **concurrent write** needs; varied/changing access patterns; or where a partition key returns too many/too few partitions.

> **Version support:** GA Delta on DBR 15.4 LTS+; PP Iceberg on DBR 16.4 LTS+. Managed Iceberg **v3** also gets deletion vectors, row tracking, row-level concurrency, and automatic LC — requires **DBR 18.0+**.

## Enable on new tables

```sql
CREATE TABLE table1 (col0 INT, col1 STRING) CLUSTER BY (col0);   -- empty
CREATE TABLE table2 CLUSTER BY (col0) AS SELECT * FROM table1;   -- from data (CLUSTER BY after name, not in SELECT)
CREATE TABLE table3 LIKE table1;                                 -- copies clustering config
```

```python
(DeltaTable.create().tableName("table1")
  .addColumn("col0", dataType="INT").addColumn("col1", dataType="STRING").clusterBy("col0").execute())
df.write.clusterBy("col0").saveAsTable("table2")
df.writeTo("table1").using("delta").clusterBy("col0").create()   # DataFrameWriterV2, DBR 14.2+
```

> **DataFrame API caveat:** clustering keys can only be set at table **creation or overwrite** (e.g. `CREATE OR REPLACE`), **not** in **append** mode — use SQL `ALTER TABLE` to change keys separately from writes.

DBR 16.4 LTS+ can create LC tables via Structured Streaming writes (`spark.readStream.table(...).writeStream.clusterBy("col").option("checkpointLocation", p).toTable(...)`).

> **Protocol warning:** Delta LC tables use writer v7 / reader v3; clients lacking these can't read them and you can't downgrade.

## Enable on existing tables

```sql
ALTER TABLE <table_name> CLUSTER BY (<clustering_columns>);
```

- Managed Iceberg **v2**: turn off deletion vectors + row tracking first. **v3**: not required.
- Does **not** cluster previously written data — force with `OPTIMIZE FULL` / `OPTIMIZE FULL WHERE <predicate>`.

## Convert a partitioned table → LC (DBR 18.1+)

```sql
ALTER TABLE <table_name> REPLACE PARTITIONED BY WITH CLUSTER BY [( <clustering_columns> ) | AUTO];
```

- `( columns )` — new keys; keep them **similar to original partition columns** (very different cols trigger a large recluster on first `OPTIMIZE`).
- `AUTO` — uses current partition cols as initial keys, lets predictive optimization adapt. **UC managed tables only.**
- no options — keeps current partition cols as keys.

Minimizes downtime; supports external + managed tables; after conversion reads work on DBR 13.3 LTS+. (Managed Iceberg: conversion unnecessary — partition defs already act as LC keys; running the command errors.) Run `OPTIMIZE` afterward to benefit. **Timestamp partition column** needs `SET spark.databricks.delta.liquidConversion.statsGeneration.enabled = false;` then `ANALYZE TABLE … COMPUTE DELTA STATISTICS` or it errors (`unsupported type: timestamp`). Verify with `DESCRIBE EXTENDED`/`DESCRIBE HISTORY`; roll back via `CLUSTER BY NONE` + `UNSET TBLPROPERTIES ('delta.liquid.hierarchicalClusteringColumns')` + `RESTORE`. **Not** supported for SDP-created streaming tables/MVs (use `CLUSTER BY` in the pipeline instead) or Delta Sharing with partition filtering.

## Remove keys

```sql
ALTER TABLE table_name CLUSTER BY NONE;
```

## Choosing clustering keys

- Pick the columns **most frequently used in query filters** — that drives data skipping. Keys can be in any order; if two columns are highly correlated, include only one.
- **Up to 4 keys.** For small tables (<10 TB), more keys can *degrade* single-column filter performance; the difference shrinks as the table grows.
- Keys must be columns with statistics (default first 32 columns). Databricks recommends `CLUSTER BY AUTO`.
- **Supported types:** Date, Timestamp, TimestampNTZ (DBR 14.3 LTS+), String, Integer/Long/Short/Byte, Float/Double/Decimal, and Struct fields via dot notation. **Not** complex types themselves or Map/Array elements.

Migrating from partitioning / Z-order:

| Current technique | Clustering keys to use |
|---|---|
| Hive-style partitioning | the partition columns |
| Z-order | the `ZORDER BY` columns |
| Partitioning + Z-order | both sets |
| Generated column to reduce cardinality | the original column; drop the generated column |

## Automatic liquid clustering (`CLUSTER BY AUTO`)

DBR 15.4 LTS+ for UC managed **Delta**; DBR 18.0+ for managed **Iceberg v3**. Also for MVs + streaming tables. Requires **predictive optimization** (runs async): analyzes historical query workload to pick keys, adapts when patterns change, and is **cost-aware** (changes keys only when predicted skipping savings outweigh clustering cost). May not select keys when the table is too small, already well-clustered, or rarely queried.

```sql
CREATE OR REPLACE TABLE table1 (column01 int, column02 string) CLUSTER BY AUTO;
ALTER TABLE table1 CLUSTER BY AUTO;       -- enable on existing
ALTER TABLE table1 CLUSTER BY (c1, c2);   -- set hint columns…
ALTER TABLE table1 CLUSTER BY AUTO;       -- …then turn on AUTO
ALTER TABLE table1 CLUSTER BY NONE;       -- turn off
```

> **`CREATE OR REPLACE` gotcha:** replacing a table **without** `CLUSTER BY AUTO` turns off automatic clustering and does **not** preserve clustering columns. Include `CLUSTER BY AUTO` in the replace to keep it.

Check status: `DESCRIBE TABLE` / `SHOW TBLPROPERTIES` → `clusterByAuto = true`, `clusteringColumns` shows keys. Not available for managed Iceberg v2 (v3 on DBR 18.0+).

## Writing to a clustered table

Operations that **cluster on write**: `INSERT INTO`, `CTAS`/`RTAS`, `COPY INTO` from Parquet, `spark.write.mode("append")`. Clustering on write only triggers above a size threshold (lower for UC managed tables):

| # clustering columns | UC managed table | Other Delta table |
|---|---|---|
| 1 | 64 MB | 256 MB |
| 2 | 256 MB | 1 GB |
| 3 | 512 MB | 2 GB |
| 4 | 1 GB | 4 GB |

Because not all ops cluster on write, run `OPTIMIZE` frequently. **Streaming:** set `spark.databricks.delta.liquid.eagerClustering.streaming.enabled = true` (triggers only if ≥1 of the last 5 streaming updates exceeds a threshold).

## Triggering clustering

> "Liquid clustering is incremental, meaning that OPTIMIZE only rewrites data as necessary to accommodate data that needs clustering."

Predictive optimization auto-runs `OPTIMIZE` on enabled tables (disable scheduled `OPTIMIZE` jobs when using it). Manual:

```sql
OPTIMIZE table_name;          -- incremental; only rewrites data needing clustering
OPTIMIZE table_name FULL;     -- force full recluster (DBR 16.4 LTS+)
OPTIMIZE events FULL WHERE event_date >= '2025-01-01';  -- partial recluster, DBR 18.1+
```

Run `OPTIMIZE FULL` on first enable or after changing keys. Without predictive optimization, schedule `OPTIMIZE` regularly (every 1–2 h for high-update tables; DBR 17.3 LTS+ recommended for faster `OPTIMIZE`).

## Reading & managing

Read with any Delta client supporting deletion vectors (Iceberg: via UC Iceberg REST Catalog API, DBR 13.3 LTS+). `DESCRIBE TABLE` / `DESCRIBE DETAIL` show keys; `ALTER TABLE … CLUSTER BY (new1, new2)` changes keys (existing data not rewritten); `CLUSTER BY NONE` stops.

## From an external engine (managed Iceberg)

External Iceberg engines specify partition columns at create → UC interprets them as clustering keys (`CREATE OR REPLACE TABLE … PARTITIONED BY c1`; `ALTER TABLE … ADD/DROP PARTITION FIELD …`; bucket transforms are dropped and the base column used as a key).

## Override default feature enablement (optional)

Turn off a Delta feature before enabling LC to avoid the protocol upgrade:

| Delta feature | Runtime compat | Property | Effect if off |
|---|---|---|---|
| Deletion vectors | RW DBR 12.2 LTS+ | `'delta.enableDeletionVectors'='false'` | Also disables row-level concurrency → more conflicts; DELETE/MERGE/UPDATE slower |
| Row tracking | Write DBR 13.3 LTS+, read any | `'delta.enableRowTracking'='false'` | Also disables row-level concurrency → more conflicts |
| Checkpoint V2 | RW DBR 13.3 LTS+ | `'delta.checkpointPolicy'='classic'` | No effect on LC behavior |

## Compatibility & limitations

LC tables created on DBR 14.3 LTS+ use **checkpoint V2** by default (readable/writable DBR 13.3 LTS+); to support readers on DBR 12.2 LTS–13.2, disable checkpoint V2 and downgrade the protocol. Other limitations: DBR ≤15.1 — clustering on write doesn't support source queries with filters/joins/aggregations; DBR ≤15.4 LTS — can't *create* an LC table via Structured Streaming write (can write to an existing one); managed Iceberg v2 has no row-level concurrency (v3 does).

Related: [[predictive-optimization]], [[ch02-managing-data-with-delta-lake]], [[optimize-data-workloads-guide]], [[aqe]], [[managed-tables]].
