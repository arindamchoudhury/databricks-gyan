# Checkpoint V2

> **Source:** [docs.databricks.com/aws/en/tables/features/checkpoint-v2](https://docs.databricks.com/aws/en/tables/features/checkpoint-v2)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** tables, delta-lake, table-features, checkpoint-v2, concurrency, transaction-log, liquid-clustering, automatic-upgrades, B4
> **Type:** documentation

## Summary

Checkpoint V2 is a Delta Lake table feature that lets a table **support more concurrent writers and cuts write conflicts** on large or frequently-updated tables. Delta periodically writes checkpoints recording the transaction-log state so query planning can reconstruct table state without replaying the full log; the V2 checkpoint format scales that mechanism for high-concurrency, hot tables. Readable/writable on DBR **13.3 LTS and above**, enabled at the **table level**, and auto-enabled for liquid-clustering tables (DBR 14.1+) and for UC managed tables via automatic upgrades.

> Breadcrumb: Tables › Table functionality › Table features › Checkpoint V2.

## Key points

- Solves a **concurrency** problem: more concurrent writers, fewer write conflicts on large/hot tables.
- Enabled per **table** via the `delta.checkpointPolicy` = `v2` property; the underlying table feature is `v2Checkpoint`.
- **DBR 13.3 LTS+** to read and write.
- **Auto-enabled** two ways: (1) tables created with liquid clustering on DBR 14.1+ use it by default; (2) [[automatic-upgrades]] can turn it on for UC managed tables.
- Open-source: defined in the Delta Lake protocol spec (checkpoint V2).
- Downgrade by dropping the `v2Checkpoint` feature (protocol downgrade).

## Notes

### What a checkpoint is

Delta Lake periodically writes checkpoints that record the state of the transaction log. Checkpoints speed up query planning by letting Delta reconstruct table state **without replaying the full transaction log**. Checkpoint V2 is a newer checkpoint format that makes this scale to more concurrent writers.

### Enable checkpoint V2

Enable at the **table level**.

**Automatic enablement**

- Tables created with **liquid clustering** on DBR **14.1+** use checkpoint V2 by default (see Compatibility for tables with liquid clustering).
- **Automatic upgrades** can turn it on for Unity Catalog managed tables — see [[automatic-upgrades]] (checkpoint V2 there: GA for new tables/new schemas, Public Preview for all tables/existing schemas, min DBR 13.3 LTS).

**Manual enablement**

On an existing Delta table:

```sql
ALTER TABLE table_name SET TBLPROPERTIES ('delta.checkpointPolicy' = 'v2');
```

On a new Delta table:

```sql
CREATE TABLE table_name (...)
TBLPROPERTIES ('delta.checkpointPolicy' = 'v2');
```

You can optionally trigger a checkpoint manually via `REORG TABLE`.

### Downgrade to classic

To downgrade to classic checkpoints and fully remove checkpoint V2:

```sql
ALTER TABLE table_name DROP FEATURE v2Checkpoint;
```

See "Drop a Delta Lake table feature and downgrade table protocol."

## Quotes worth keeping

> "Checkpoint V2 allows Delta Lake to support more concurrent writers and reduces write conflicts on large or frequently updated tables." (intro)

## Open questions

- Property name is `delta.checkpointPolicy='v2'` but the droppable table feature is `v2Checkpoint` — the page doesn't spell out the relationship beyond "drop the feature to remove it."

## Related sources

- [[automatic-upgrades]] — lists checkpoint V2 as one of the six auto-enabled managed-table features (GA new / PP existing, min DBR 13.3 LTS); this note is the standalone explanation it name-drops.
- [[liquid-clustering]] — LC tables on DBR 14.1+ enable checkpoint V2 by default.
- [[transactions]] — checkpoint V2's concurrency benefit sits under the same multi-writer concern that catalog commits/transactions address from the metadata side.
- [[catalog-commits]] — sibling concurrency/commit mechanism; catalog commits moves commit coordination to UC, checkpoint V2 scales the log-checkpoint format.
