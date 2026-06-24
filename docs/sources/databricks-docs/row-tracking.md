# Row tracking

> **Source:** [docs.databricks.com/aws/en/tables/features/row-tracking](https://docs.databricks.com/aws/en/tables/features/row-tracking)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** tables, delta, iceberg, row-tracking, row-id, row-commit-version, row-lineage, delta-protocol, materialized-views, change-data-feed, I5
> **Type:** documentation

## Summary

Row tracking adds **row-level lineage** to a table via two hidden metadata fields — `_metadata.row_id` (a stable unique row identifier) and `_metadata.row_commit_version` (the version a row was last inserted/updated). It's the **substrate** other features build on: required for some materialized-view incremental updates, and the prerequisite for **automatic change data feed**. **Iceberg v3 tables include it automatically**; Delta tables must enable `delta.enableRowTracking`. It's a writer-protocol-bumping table feature — a one-way door on the protocol.

> Breadcrumb: Tables › Table functionality › Table features › Row tracking. DBR 14.1+. Enabling backfills row IDs to every existing row (can be slow).

## Key points

- Two hidden fields: **`_metadata.row_id`** (Long, stable across MERGE/UPDATE) and **`_metadata.row_commit_version`** (Long, bumps on each MERGE/UPDATE). Add them explicitly to a query to return them.
- **Iceberg v3 → always on.** Delta → opt-in `delta.enableRowTracking=true`.
- **DBR 14.1+.** Writer-protocol bump — **protocol can't be downgraded**, and clients lacking the writer features **can't write** the table.
- Enabling on an **existing** table **assigns IDs to all existing rows** → may create many new table versions and take significant time.
- **Cloning creates separate history** → cloned-table row IDs/versions don't match the original.
- **Disabling is half a no-op:** `=false` does **not** remove the table feature, downgrade the protocol, or drop the metadata fields — and IDs are no longer reliable afterward.
- **Limitation:** the row-tracking metadata fields **can't be read from the change data feed**.

## Notes

### Enable

```sql
-- new table
CREATE TABLE table_name
TBLPROPERTIES (delta.enableRowTracking = true)
AS SELECT * FROM source_table;

-- existing table (backfills IDs to all rows — can be slow, many new versions)
ALTER TABLE table_name SET TBLPROPERTIES (delta.enableRowTracking = true);
```

### Metadata fields

| Field | Type | Meaning |
|---|---|---|
| `_metadata.row_id` | Long | Unique row identifier; **stays the same** when the row is modified via MERGE/UPDATE. |
| `_metadata.row_commit_version` | Long | Delta log/table version the row was last inserted or updated at; **new version on each** MERGE/UPDATE. |

`OPTIMIZE` / `REORG` on a row-tracking table rewrites data files to materialize these fields (otherwise some ops store them via the transaction log).

### Disable

```sql
ALTER TABLE table_name SET TBLPROPERTIES (delta.enableRowTracking = false);
```

> Disabling **doesn't** remove the table feature, **doesn't** downgrade the protocol, **doesn't** drop the metadata fields. With it off, generated row IDs are no longer reliable for tracking unique rows.

## Quotes worth keeping

> "A row keeps the same ID whenever it is modified using a MERGE or UPDATE statement." (`_metadata.row_id`)

> "Disabling row tracking doesn't remove the corresponding table feature and doesn't downgrade the table protocol version. It also doesn't remove the metadata fields from the target table." (Disable row tracking)

## Open questions

- "Some incremental updates for materialized views require this feature" — which MV update paths specifically isn't enumerated here.

## Related sources

- [[change-data-feed]] — automatic CDF **requires row tracking** (Delta) / row lineage (Iceberg v3); yet the row-tracking metadata fields themselves can't be read *from* the CDF.
- [[automatic-upgrades]] — row tracking is one of the six auto-upgradeable features (min DBR 14.3 LTS); enabling it also makes automatic CDF available.
- [[liquid-clustering]] — row-level concurrency (fewer write conflicts) is tied to deletion vectors + row tracking.
- [[tables-concepts]] — Delta protocol versions / feature compatibility; row tracking is a one-way protocol bump.
