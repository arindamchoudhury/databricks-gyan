# Isolation levels and write conflicts

> **Source:** [docs.databricks.com/aws/en/optimizations/isolation-level](https://docs.databricks.com/aws/en/optimizations/isolation-level)
> **Added:** 2026-06-24
> **Source updated:** 2026-03-09
> **Tags:** optimization, delta, isolation, write-serializable, serializable, concurrency, write-conflicts, acid, row-level-concurrency, streaming, A1, B4
> **Type:** documentation

## Summary
Overview of Delta Lake isolation + write-conflict behavior. Delta gives ACID guarantees between reads and writes: multiple writers across clusters can modify a table partition simultaneously, see a consistent snapshot, and writes occur in serial order; readers see a consistent snapshot from when the job started, even if the table is modified mid-job. Two isolation levels — **`WriteSerializable` (default)** and **`Serializable`** — plus row-level concurrency. Delta is the default format for all Databricks tables.

## Key points

- Two levels: **`WriteSerializable`** (default, more concurrency) vs **`Serializable`** (stricter read-serializability, can reduce concurrent-write throughput).
- Set per table: `ALTER TABLE … SET TBLPROPERTIES ('delta.isolationLevel' = 'Serializable')`.
- **Row-level concurrency** reduces write conflicts on the same files (tied to deletion vectors + row tracking).
- **Metadata changes fail all concurrent writes** and **break streaming reads** (must restart the stream).

## Notes

### Isolation topics (links from this page)

- **Isolation levels (WriteSerializable and Serializable)** — how the two levels affect concurrent ops + how to configure.
- **Row-level concurrency** — row-level conflict detection reduces conflicts for concurrent ops on the same data files. See also [[liquid-clustering]] (deletion vectors / row tracking enable it).

For transaction isolation, snapshot behavior, and conflict handling, see [[transactions]].

### Metadata change conflicts

Metadata changes make **all concurrent write operations fail**. These include changes to **table protocol, table properties, or data schema**. **Streaming reads fail** on a commit that changes metadata — restart the stream to continue.

Example metadata-changing queries:

```sql
-- Set a table property (incl. the isolation level itself)
ALTER TABLE table_name SET TBLPROPERTIES ('delta.isolationLevel' = 'Serializable');

-- Enable a feature + update protocol
ALTER TABLE table_name SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);

-- Drop a table feature
ALTER TABLE table_name DROP FEATURE deletionVectors;

-- Upgrade to UniForm
REORG TABLE table_name APPLY (UPGRADE UNIFORM(ICEBERG_COMPAT_VERSION=2));

-- Update schema
ALTER TABLE table_name ADD COLUMNS (col_name STRING);
```

> **Practical note:** flipping `delta.isolationLevel` on a live table is itself a metadata change → it fails in-flight concurrent writes and breaks active streams. Schedule it during a quiet window.

## Quotes worth keeping

> "Multiple writers across multiple clusters can simultaneously modify a table partition. Writers see a consistent snapshot view of the table and writes occur in a serial order." (intro)

> "Metadata changes cause all concurrent write operations to fail." (Metadata change conflicts)

## Open questions

- This page is an index — the actual WriteSerializable-vs-Serializable semantics + the full conflict matrix live on the linked "Transaction isolation" page (not captured here; see [[transactions]] for the multi-statement-transaction angle).

## Related sources

- [[transactions]] — multi-statement ACID transactions + the concurrency/conflict model this references.
- [[liquid-clustering]] — deletion vectors + row tracking that power row-level concurrency.
- [[optimization-recommendations]] — parent hub (lists isolation under opt-in behaviors).
