# Checkpoint V2

> **Source:** [docs.databricks.com/aws/en/tables/features/checkpoint-v2](https://docs.databricks.com/aws/en/tables/features/checkpoint-v2)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** tables, delta-lake, table-features, checkpoint-v2, concurrency, transaction-log, liquid-clustering, automatic-upgrades, B4
> **Type:** documentation

Checkpoint V2 is a Delta Lake table feature that lets a table **support more concurrent writers and cuts write conflicts** on large or frequently-updated tables. Delta periodically writes checkpoints recording the transaction-log state so query planning can reconstruct table state **without replaying the full log**; the V2 checkpoint format scales that mechanism for high-concurrency, hot tables. It's readable/writable on DBR **13.3 LTS+**, enabled at the **table level** via `delta.checkpointPolicy = 'v2'` (the underlying table feature is `v2Checkpoint`), and defined in the open Delta Lake protocol spec.

> "Checkpoint V2 allows Delta Lake to support more concurrent writers and reduces write conflicts on large or frequently updated tables."

## Enable checkpoint V2

**Automatic enablement:**

- Tables created with **liquid clustering** on DBR **14.1+** use checkpoint V2 by default ([[liquid-clustering]]).
- **Automatic upgrades** can turn it on for UC managed tables — see [[automatic-upgrades]] (GA for new tables/new schemas, Public Preview for all tables/existing schemas, min DBR 13.3 LTS).

**Manual enablement:**

```sql
ALTER TABLE table_name SET TBLPROPERTIES ('delta.checkpointPolicy' = 'v2');   -- existing
CREATE TABLE table_name (...) TBLPROPERTIES ('delta.checkpointPolicy' = 'v2'); -- new
```

You can optionally trigger a checkpoint manually via `REORG TABLE`.

## Downgrade to classic

```sql
ALTER TABLE table_name DROP FEATURE v2Checkpoint;
```

See "Drop a Delta Lake table feature and downgrade table protocol."

Related: [[automatic-upgrades]], [[liquid-clustering]], [[transactions]], [[catalog-commits]].
