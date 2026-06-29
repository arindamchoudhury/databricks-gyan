# Upsert into a Delta Lake table using merge

> **Source:** [docs.databricks.com/aws/en/delta/merge](https://docs.databricks.com/aws/en/delta/merge)
> **Added:** 2026-06-29
> **Source updated:** 2026-06-11
> **Tags:** delta, merge, upsert, scd, deduplication, when-matched, when-not-matched-by-source, incremental-sync, foreachBatch, I5, I4
> **Type:** documentation

`MERGE INTO` upserts data from a source table, view, or DataFrame into a target Delta Lake table — handling inserts, updates, and deletes in one atomic operation. Delta extends standard SQL MERGE with `WHEN NOT MATCHED BY SOURCE` and other capabilities.

## Python DataFrame API

The Python API chains builder methods on a `DeltaTable` object and requires `.execute()` at the end:

| SQL clause | Python method |
|---|---|
| `WHEN MATCHED THEN UPDATE SET col=val` | `.whenMatchedUpdate(condition=..., set={...})` |
| `WHEN MATCHED THEN UPDATE SET *` | `.whenMatchedUpdateAll()` |
| `WHEN MATCHED THEN DELETE` | `.whenMatchedDelete(condition=...)` |
| `WHEN NOT MATCHED THEN INSERT (cols) VALUES (vals)` | `.whenNotMatchedInsert(condition=..., values={...})` |
| `WHEN NOT MATCHED THEN INSERT *` | `.whenNotMatchedInsertAll()` |
| `WHEN NOT MATCHED BY SOURCE THEN UPDATE SET col=val` | `.whenNotMatchedBySourceUpdate(condition=..., set={...})` |
| `WHEN NOT MATCHED BY SOURCE THEN DELETE` | `.whenNotMatchedBySourceDelete(condition=...)` |

Basic upsert:

```python
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "people10m")
updates = spark.table("people10mupdates")

(target.alias("people")
  .merge(updates.alias("updates"), "people.id = updates.id")
  .whenMatchedUpdate(set={"firstName": "updates.firstName", "salary": "updates.salary"})
  .whenNotMatchedInsert(values={"id": "updates.id", "firstName": "updates.firstName", "salary": "updates.salary"})
  .execute()
)
```

With `WHEN NOT MATCHED BY SOURCE` (DBR 12.2 LTS+):

```python
(targetDF
  .merge(sourceDF, "source.key = target.key")
  .whenMatchedUpdate(set={"target.lastSeen": "source.timestamp"})
  .whenNotMatchedInsert(values={"target.key": "source.key", "target.lastSeen": "source.timestamp", "target.status": "'active'"})
  .whenNotMatchedBySourceUpdate(
    condition="target.lastSeen >= (current_date() - INTERVAL '5' DAY)",
    set={"target.status": "'inactive'"}
  )
  .execute()
)
```

Column values in `set`/`values` dicts are **SQL expression strings** (not Python values) — string literals need inner quotes: `"'active'"`.

## Basic upsert (SQL)

```sql
MERGE INTO people10m
USING people10mupdates
ON people10m.id = people10mupdates.id
WHEN MATCHED THEN
  UPDATE SET id = people10mupdates.id, firstName = people10mupdates.firstName, ...
WHEN NOT MATCHED THEN
  INSERT (id, firstName, ...) VALUES (people10mupdates.id, people10mupdates.firstName, ...)
```

**Important:** Only a single source row can match a given target row. In **DBR 16.0+**, MERGE evaluates conditions in both the `WHEN MATCHED` and `ON` clauses to detect duplicate matches. In **DBR 15.4 LTS and below**, only the `ON` clause is used — a source with multiple rows matching the same target key will fail on those older runtimes if any `WHEN MATCHED` condition is also true for more than one.

`MERGE` on a SQL VIEW is only supported when the view is defined as `CREATE VIEW viewName AS SELECT * FROM deltaTable`.

## WHEN NOT MATCHED BY SOURCE (DBR 12.2 LTS+)

Modify target rows that have **no corresponding source row** — useful for syncing or pruning stale records:

```sql
MERGE INTO target
USING source ON source.key = target.key
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE THEN DELETE
```

**Always add a condition** to `WHEN NOT MATCHED BY SOURCE` to avoid fully rewriting the target table:

```sql
WHEN NOT MATCHED BY SOURCE AND target.lastSeen >= (current_date() - INTERVAL '5' DAY)
  THEN UPDATE SET target.status = 'inactive'
```

`WHEN NOT MATCHED BY SOURCE` clauses **cannot reference source columns** (there is no matching source row); actions must use literals or expressions on target columns only (e.g. `SET target.deleted_count = target.deleted_count + 1`).

## Merge operation semantics

**`whenMatched` clauses** (source row matches a target row):
- At most one `update` and one `delete` action.
- Each clause can have an optional condition; if none evaluate to true, the target row is left unchanged.
- Multiple clauses evaluated in order; all except the last must have conditions.
- `updateAll()` / `UPDATE SET *` maps source columns to target columns by name — requires matching schemas (or use automatic schema evolution).

**`whenNotMatched` clauses** (source row has no matching target row):
- INSERT action only. Unspecified target columns receive `NULL`.
- Multiple clauses evaluated in order; all except the last must have conditions.
- `insertAll()` / `INSERT *` requires matching schemas.

**`whenNotMatchedBySource` clauses** (target row has no matching source row):
- UPDATE or DELETE actions.
- Cannot reference source columns.
- Multiple clauses evaluated in order; all except the last must have conditions.

## Deduplication pattern

Insert-only merge: inserts source rows only if no match exists in the target. Source must already be deduplicated within itself — MERGE won't deduplicate across new rows.

```sql
MERGE INTO logs
USING newDedupedLogs ON logs.uniqueId = newDedupedLogs.uniqueId
WHEN NOT MATCHED THEN INSERT *
```

For large tables where duplicates are time-bounded, scope the match to a recent window to avoid scanning the full target:

```sql
MERGE INTO logs
USING newDedupedLogs
ON logs.uniqueId = newDedupedLogs.uniqueId
   AND logs.date > current_date() - INTERVAL 7 DAYS
WHEN NOT MATCHED AND newDedupedLogs.date > current_date() - INTERVAL 7 DAYS
  THEN INSERT *
```

This insert-only merge can be used with Structured Streaming via `foreachBatch` for **continuous deduplication** — the target is append-only from the MERGE perspective, so a second stream can safely read from it.

## SCD and CDC

For **Slowly Changing Dimensions (SCD Type 1/2)** and **Change Data Capture (CDC)**, prefer `AUTO CDC ... INTO` in Lakeflow Spark Declarative Pipelines — it handles out-of-order records correctly. See [[what-is-cdc]].

## Incrementally sync with source (DBR 12.2 LTS+)

Use `WHEN NOT MATCHED BY SOURCE` with a date filter on both source and target to atomically propagate changes (including deletes) for a bounded window, without rewriting the whole table:

```sql
MERGE INTO target AS t
USING (SELECT * FROM source WHERE created_at >= (current_date() - INTERVAL '5' DAY)) AS s
ON t.key = s.key
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE AND created_at >= (current_date() - INTERVAL '5' DAY) THEN DELETE
```

The same boolean filter on source and target ensures only the bounded window is touched — unmatched records outside that window are left alone.

[change-data-feed](change-data-feed.md) · [what-is-cdc](what-is-cdc.md) · [low-shuffle-merge](low-shuffle-merge.md) · [row-tracking](row-tracking.md)
