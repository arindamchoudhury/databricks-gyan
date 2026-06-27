# Isolation levels and write conflicts

> **Source:** [docs.databricks.com/aws/en/optimizations/isolation-level](https://docs.databricks.com/aws/en/optimizations/isolation-level)
> **Added:** 2026-06-24
> **Source updated:** 2026-03-09
> **Tags:** optimization, delta, isolation, write-serializable, serializable, concurrency, write-conflicts, acid, row-level-concurrency, streaming, A1, B4
> **Type:** documentation

> "Multiple writers across multiple clusters can simultaneously modify a table partition. Writers see a consistent snapshot view of the table and writes occur in a serial order."

Delta gives ACID guarantees between reads and writes: writers see a consistent snapshot and commit in serial order; readers see a consistent snapshot from when the job started, even if the table is modified mid-job. Two isolation levels exist — **`WriteSerializable`** (default, more concurrency) and **`Serializable`** (stricter read-serializability, can reduce concurrent-write throughput) — plus **row-level concurrency** (tied to deletion vectors + row tracking), which reduces write conflicts on the same files. Set the level per table: `ALTER TABLE … SET TBLPROPERTIES ('delta.isolationLevel' = 'Serializable')`.

For the full WriteSerializable-vs-Serializable semantics and conflict matrix, see the "Transaction isolation" page and [[transactions]].

## Metadata change conflicts

> "Metadata changes cause all concurrent write operations to fail."

Changes to **table protocol, table properties, or data schema** fail all concurrent writes, and **streaming reads fail** on a commit that changes metadata (restart the stream). Example metadata-changing queries:

```sql
ALTER TABLE table_name SET TBLPROPERTIES ('delta.isolationLevel' = 'Serializable');   -- the level itself
ALTER TABLE table_name SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);      -- enable a feature
ALTER TABLE table_name DROP FEATURE deletionVectors;
REORG TABLE table_name APPLY (UPGRADE UNIFORM(ICEBERG_COMPAT_VERSION=2));              -- upgrade to UniForm
ALTER TABLE table_name ADD COLUMNS (col_name STRING);                                 -- update schema
```

> **Practical note:** flipping `delta.isolationLevel` on a live table is itself a metadata change → it fails in-flight concurrent writes and breaks active streams. Schedule it during a quiet window.

Related: [[transactions]], [[liquid-clustering]], [[optimization-recommendations]].
