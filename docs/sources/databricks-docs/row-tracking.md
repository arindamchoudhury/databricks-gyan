# Row tracking

> **Source:** [docs.databricks.com/aws/en/tables/features/row-tracking](https://docs.databricks.com/aws/en/tables/features/row-tracking)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** tables, delta, iceberg, row-tracking, row-id, row-commit-version, row-lineage, delta-protocol, materialized-views, change-data-feed, I5
> **Type:** documentation

Row tracking adds **row-level lineage** to a table via two hidden metadata fields — `_metadata.row_id` (a stable unique row identifier) and `_metadata.row_commit_version` (the version a row was last inserted/updated). It's the **substrate** other features build on: required for some materialized-view incremental updates, and the prerequisite for **automatic change data feed** ([[change-data-feed]]). **Iceberg v3 tables include it automatically**; Delta tables must enable `delta.enableRowTracking` (DBR **14.1+**). It's a writer-protocol-bumping table feature — a one-way door: the **protocol can't be downgraded**, clients lacking the writer features **can't write** the table, and enabling on an existing table **backfills row IDs to every existing row** (can create many new versions and take significant time).

## Enable

```sql
CREATE TABLE table_name TBLPROPERTIES (delta.enableRowTracking = true) AS SELECT * FROM source_table;  -- new
ALTER TABLE table_name SET TBLPROPERTIES (delta.enableRowTracking = true);                             -- existing (backfills)
```

## Metadata fields

Add them explicitly to a query to return them.

| Field | Type | Meaning |
|---|---|---|
| `_metadata.row_id` | Long | Unique row identifier; **stays the same** when the row is modified via MERGE/UPDATE. |
| `_metadata.row_commit_version` | Long | Table version the row was last inserted/updated at; **new version on each** MERGE/UPDATE. |

> "A row keeps the same ID whenever it is modified using a MERGE or UPDATE statement."

`OPTIMIZE` / `REORG` on a row-tracking table rewrites data files to materialize these fields (otherwise some ops store them via the transaction log).

## Disable

```sql
ALTER TABLE table_name SET TBLPROPERTIES (delta.enableRowTracking = false);
```

> "Disabling row tracking doesn't remove the corresponding table feature and doesn't downgrade the table protocol version. It also doesn't remove the metadata fields from the target table." With it off, generated row IDs are no longer reliable for tracking unique rows.

Two more notes: **cloning creates separate history** (cloned-table row IDs/versions don't match the original), and the row-tracking metadata fields **can't be read from the change data feed**.

Related: [[change-data-feed]], [[automatic-upgrades]], [[liquid-clustering]], [[tables-concepts]].
