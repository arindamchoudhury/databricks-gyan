# Column mapping (rename & drop columns)

> **Source:** [docs.databricks.com/aws/en/tables/features/column-mapping](https://docs.databricks.com/aws/en/tables/features/column-mapping)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-23
> **Tags:** tables, delta, column-mapping, rename-column, drop-column, schema-evolution, delta-protocol, streaming, schema-tracking-location, uniform, I5, A4
> **Type:** documentation

## Summary

Delta Lake **column mapping** lets you **rename and drop columns as metadata-only changes** — no data-file rewrite — and allows Parquet-illegal characters (spaces, `,;{}()\n\t=`) in column names so you can ingest CSV/JSON directly without renaming. Controlled by the `delta.columnMapping.mode` table property (`none` default / `name` / `id`). It bumps the Delta protocol (reader v2+, writer v5+) and **breaks** several path/streaming/CDF assumptions, so enabling it is a real decision, not a free switch.

> Breadcrumb: Tables › Table functionality › Table features › Column mapping. Delta-only. The feature behind the non-additive-schema-change limitation noted in [[change-data-feed]].

## Key points

- **Metadata-only rename/drop** — `ALTER TABLE … RENAME COLUMN` (DBR 10.4 LTS+) and `DROP COLUMN[S]` (DBR 11.3 LTS+) without rewriting data.
- Allows **special characters** in column names (spaces, `,;{}()\n\t=`) → direct CSV/JSON ingest.
- **Modes:** `none` (default, Parquet naming rules) · `name` (new **or** existing tables) · `id` (**creation-only**, can't set on existing). Databricks **recommends `id`**; `name` is auto-set if you enable UniForm/Iceberg compat without specifying a mode.
- **Protocol bump:** reader v2+, writer v5+ → tables only readable on **DBR 10.4 LTS+**.
- **Enabling can break:** legacy directory-name-based reads (partitioned tables use **random prefixes**, not column names), **Delta CDF** downstream ops, and **streaming reads** (incl. Lakeflow SDP) — fix streaming with a `schemaTrackingLocation`.
- **Removing it rewrites all data files** (logical→physical names) — no row-level conflict resolution, throws `ConcurrentModificationException` under concurrent writes. Prefer `DROP FEATURE` (DBR 15.3+) if you need a protocol downgrade.

## Notes

### Enable

```sql
-- id mode, new table only
CREATE TABLE <table-name> (id INT, name STRING)
USING DELTA
TBLPROPERTIES ('delta.columnMapping.mode' = 'id');

-- name mode, existing table
ALTER TABLE <table-name> SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name');
```

Requires Delta **reader v2+ / writer v5+**.

### Rename / drop

```sql
ALTER TABLE <table-name> RENAME COLUMN old_col_name TO new_col_name;          -- DBR 10.4 LTS+
ALTER TABLE table_name DROP COLUMN col_name;                                   -- DBR 11.3 LTS+
ALTER TABLE table_name DROP COLUMNS (col_name_1, col_name_2);
```

### Modes

| Mode | Metadata rename/drop | Special chars | Settable on |
|---|---|---|---|
| `none` (default) | no | no (Parquet rules) | — |
| `name` | yes | yes | new **and** existing tables |
| `id` | yes | yes | **table creation only** |

`id` recommended for compatibility. `name` auto-applied if `delta.columnMapping.mode` is unset and you enable Iceberg-compat features like **UniForm**.

### Remove vs disable

```sql
-- remove: rewrites ALL data files (logical -> physical names)
ALTER TABLE <table-name> SET TBLPROPERTIES ('delta.columnMapping.mode' = 'none');
```

> ⚠️ Remove rewrites every file, no row-level/physical conflict resolution → concurrent writes raise `ConcurrentModificationException`. Before removing: **pause all concurrent writes** (streaming + ETL), **disable predictive optimization** on the table, and schedule during low activity for big tables.

**Disable (protocol downgrade)** — DBR 15.3+: use `DROP FEATURE` instead when you need older-reader compatibility. Note: dropping column mapping **does not remove** the random directory prefixes on partitioned tables.

### Streaming with column mapping

Non-additive schema changes (rename/drop) can break streams. Fix: give each streaming read a **`schemaTrackingLocation`** inside the write's `checkpointLocation` (unique subdir per source table for multi-source streams).

```python
checkpoint_path = "/path/to/checkpointLocation"
(spark.readStream
  .option("schemaTrackingLocation", checkpoint_path)
  .table("delta_source_table")
  .writeStream
  .option("checkpointLocation", checkpoint_path)
  .toTable("output_table"))
```

**Enable column mapping on a running streaming job** (specific dance):

1. Stop the job.
2. Enable column mapping on the table.
3. Restart (1st — initializes column mapping).
4. Restart again (2nd — enables schema changes).

Any further schema change (add/drop column, type change) also requires a restart.

## Quotes worth keeping

> "Removing column mapping rewrites all data files to replace physical column names with logical names. This operation doesn't support row-level or physical conflict resolution." (Remove column mapping)

## Open questions

- Interaction with automatic upgrades: column mapping is a PP auto-upgrade feature (min DBR 15.4 LTS per [[automatic-upgrades]]) — does auto-enable pick `name` or `id`? Not stated here.

## Related sources

- [[change-data-feed]] — column mapping's rename/drop are the **non-additive schema changes** that CDF queries can't span; automatic CDF is unsupported on such tables across the change.
- [[automatic-upgrades]] — column mapping is one of the six auto-upgradeable features (PP, min DBR 15.4 LTS).
- [[liquid-clustering]] / [[catalog-commits]] / [[transactions]] — sibling Delta features under Table functionality.
- [[tables-concepts]] — Delta protocol versions and feature compatibility context.
