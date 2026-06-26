# Column mapping (rename & drop columns)

> **Source:** [docs.databricks.com/aws/en/tables/features/column-mapping](https://docs.databricks.com/aws/en/tables/features/column-mapping)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-23
> **Tags:** tables, delta, column-mapping, rename-column, drop-column, schema-evolution, delta-protocol, streaming, schema-tracking-location, uniform, I5, A4
> **Type:** documentation

Delta Lake **column mapping** lets you **rename and drop columns as metadata-only changes** — no data-file rewrite — and allows Parquet-illegal characters (spaces, `,;{}()\n\t=`) in column names so you can ingest CSV/JSON directly without renaming. It's controlled by the `delta.columnMapping.mode` table property and bumps the Delta protocol (reader v2+, writer v5+), so enabling it is a real decision: it **breaks** several path/streaming/CDF assumptions. Delta-only. It's the feature behind the non-additive-schema-change limitation in [[change-data-feed]].

Things it can break when enabled: legacy directory-name-based reads (partitioned tables use **random prefixes**, not column names), **Delta CDF** downstream ops, and **streaming reads** (incl. Lakeflow SDP — fix with a `schemaTrackingLocation`).

## Enable

```sql
CREATE TABLE <table-name> (id INT, name STRING) USING DELTA
  TBLPROPERTIES ('delta.columnMapping.mode' = 'id');                 -- id mode, new table only
ALTER TABLE <table-name> SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name');  -- name mode, existing
```

Requires Delta **reader v2+ / writer v5+** → tables only readable on **DBR 10.4 LTS+**.

## Rename / drop

```sql
ALTER TABLE <table-name> RENAME COLUMN old_col_name TO new_col_name;   -- DBR 10.4 LTS+
ALTER TABLE table_name DROP COLUMN col_name;                            -- DBR 11.3 LTS+
ALTER TABLE table_name DROP COLUMNS (col_name_1, col_name_2);
```

## Modes

| Mode | Metadata rename/drop | Special chars | Settable on |
|---|---|---|---|
| `none` (default) | no | no (Parquet rules) | — |
| `name` | yes | yes | new **and** existing tables |
| `id` | yes | yes | **table creation only** |

Databricks **recommends `id`** for compatibility. `name` is auto-applied if `delta.columnMapping.mode` is unset and you enable Iceberg-compat features like **UniForm**.

## Remove vs disable

```sql
ALTER TABLE <table-name> SET TBLPROPERTIES ('delta.columnMapping.mode' = 'none');  -- remove: rewrites ALL files
```

> ⚠️ "Removing column mapping rewrites all data files to replace physical column names with logical names. This operation doesn't support row-level or physical conflict resolution." → concurrent writes raise `ConcurrentModificationException`. Before removing: **pause all concurrent writes** (streaming + ETL), **disable predictive optimization** on the table, and schedule during low activity for big tables.

To downgrade the protocol for older-reader compatibility, prefer `DROP FEATURE` (DBR 15.3+). Note: dropping column mapping **does not remove** the random directory prefixes on partitioned tables.

## Streaming with column mapping

Non-additive schema changes (rename/drop) can break streams. Fix: give each streaming read a **`schemaTrackingLocation`** inside the write's `checkpointLocation` (a unique subdir per source table for multi-source streams).

```python
checkpoint_path = "/path/to/checkpointLocation"
(spark.readStream.option("schemaTrackingLocation", checkpoint_path).table("delta_source_table")
  .writeStream.option("checkpointLocation", checkpoint_path).toTable("output_table"))
```

To **enable column mapping on a running streaming job**: (1) stop the job; (2) enable column mapping on the table; (3) restart once (initializes column mapping); (4) restart again (enables schema changes). Any further schema change also requires a restart.

Related: [[change-data-feed]], [[automatic-upgrades]], [[liquid-clustering]], [[catalog-commits]], [[transactions]], [[tables-concepts]].
