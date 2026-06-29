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
| `WHEN MATCHED THEN UPDATE SET target.lastSeen = source.timestamp` | `.whenMatchedUpdate(set={"target.lastSeen": "source.timestamp"})` |
| `WHEN MATCHED THEN UPDATE SET *` | `.whenMatchedUpdateAll()` |
| `WHEN MATCHED THEN DELETE` | `.whenMatchedDelete(condition=...)` |
| `WHEN NOT MATCHED THEN INSERT (target.key, target.lastSeen, target.status) VALUES (source.key, source.timestamp, 'active')` | `.whenNotMatchedInsert(values={"target.key": "source.key", "target.lastSeen": "source.timestamp", "target.status": "'active'"})` |
| `WHEN NOT MATCHED THEN INSERT *` | `.whenNotMatchedInsertAll()` |
| `WHEN NOT MATCHED BY SOURCE AND target.lastSeen >= (current_date() - INTERVAL '5' DAY) THEN UPDATE SET target.status = 'inactive'` | `.whenNotMatchedBySourceUpdate(condition="target.lastSeen >= (current_date() - INTERVAL '5' DAY)", set={"target.status": "'inactive'"})` |
| `WHEN NOT MATCHED BY SOURCE THEN DELETE` | `.whenNotMatchedBySourceDelete(condition=...)` |

Column values in `set`/`values` dicts are **SQL expression strings** (not Python values) — string literals need inner quotes: `"'active'"`.

## Basic upsert

```sql
MERGE INTO people10m
USING people10mupdates
ON people10m.id = people10mupdates.id
WHEN MATCHED THEN
  UPDATE SET firstName = people10mupdates.firstName, salary = people10mupdates.salary
WHEN NOT MATCHED THEN
  INSERT (id, firstName, salary)
  VALUES (people10mupdates.id, people10mupdates.firstName, people10mupdates.salary)
```

```python
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "people10m")
updates = spark.table("people10mupdates")

(target.alias("people")
  .merge(updates.alias("updates"), "people.id = updates.id")
  .whenMatchedUpdate(set={"firstName": "updates.firstName", "salary": "updates.salary"})
  .whenNotMatchedInsert(values={
      "id": "updates.id",
      "firstName": "updates.firstName",
      "salary": "updates.salary",
  })
  .execute()
)
```

**Important:** Only a single source row can match a given target row. In **DBR 16.0+**, MERGE evaluates conditions in both the `WHEN MATCHED` and `ON` clauses to detect duplicate matches. In **DBR 15.4 LTS and below**, only the `ON` clause is used.

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

**Always add a condition** to `WHEN NOT MATCHED BY SOURCE` to avoid fully rewriting the target table. `WHEN NOT MATCHED BY SOURCE` clauses **cannot reference source columns** — actions must use literals or target-column expressions only:

```sql
WHEN NOT MATCHED BY SOURCE AND target.lastSeen >= (current_date() - INTERVAL '5' DAY)
  THEN UPDATE SET target.status = 'inactive'
```

```python
(targetDF
  .merge(sourceDF, "source.key = target.key")
  .whenMatchedUpdate(set={"target.lastSeen": "source.timestamp"})
  .whenNotMatchedInsert(values={
      "target.key": "source.key",
      "target.lastSeen": "source.timestamp",
      "target.status": "'active'",
  })
  .whenNotMatchedBySourceUpdate(
      condition="target.lastSeen >= (current_date() - INTERVAL '5' DAY)",
      set={"target.status": "'inactive'"},
  )
  .execute()
)
```

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

Insert-only merge: inserts source rows only if no match exists in the target. Source must already be deduplicated within itself.

```sql
MERGE INTO logs
USING newDedupedLogs ON logs.uniqueId = newDedupedLogs.uniqueId
WHEN NOT MATCHED THEN INSERT *
```

```python
(DeltaTable.forName(spark, "logs").alias("logs")
  .merge(newDedupedLogs.alias("newLogs"), "logs.uniqueId = newLogs.uniqueId")
  .whenNotMatchedInsertAll()
  .execute()
)
```

For large tables, scope the match to a recent window to avoid scanning the full target:

```sql
MERGE INTO logs
USING newDedupedLogs
ON logs.uniqueId = newDedupedLogs.uniqueId
   AND logs.date > current_date() - INTERVAL 7 DAYS
WHEN NOT MATCHED AND newDedupedLogs.date > current_date() - INTERVAL 7 DAYS
  THEN INSERT *
```

```python
(DeltaTable.forName(spark, "logs").alias("logs")
  .merge(
      newDedupedLogs.alias("newLogs"),
      "logs.uniqueId = newLogs.uniqueId AND logs.date > current_date() - INTERVAL 7 DAYS",
  )
  .whenNotMatchedInsert(
      condition="newLogs.date > current_date() - INTERVAL 7 DAYS",
      values="*",
  )
  .execute()
)
```

Use with Structured Streaming via `foreachBatch` for **continuous deduplication**:

```python
def merge_dedup(batch_df, batch_id):
    (DeltaTable.forName(spark, "logs").alias("logs")
      .merge(batch_df.alias("newLogs"), "logs.uniqueId = newLogs.uniqueId")
      .whenNotMatchedInsertAll()
      .execute()
    )

stream.writeStream.foreachBatch(merge_dedup).start()
```

## SCD and CDC

For **Slowly Changing Dimensions (SCD Type 1/2)** and **Change Data Capture (CDC)**, prefer `AUTO CDC ... INTO` in Lakeflow Spark Declarative Pipelines — it handles out-of-order records correctly. See [what-is-cdc](what-is-cdc/).

## Incrementally sync with source (DBR 12.2 LTS+)

Use `WHEN NOT MATCHED BY SOURCE` with a date filter on both source and target to atomically propagate changes (including deletes) for a bounded window, without rewriting the whole table:

```sql
MERGE INTO target AS t
USING (SELECT * FROM source WHERE created_at >= (current_date() - INTERVAL '5' DAY)) AS s
ON t.key = s.key
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE AND t.created_at >= (current_date() - INTERVAL '5' DAY) THEN DELETE
```

```python
source_df = spark.table("source").filter(
    "created_at >= (current_date() - INTERVAL '5' DAY)"
)

(DeltaTable.forName(spark, "target").alias("t")
  .merge(source_df.alias("s"), "t.key = s.key")
  .whenMatchedUpdateAll()
  .whenNotMatchedInsertAll()
  .whenNotMatchedBySourceDelete(
      condition="t.created_at >= (current_date() - INTERVAL '5' DAY)"
  )
  .execute()
)
```

The same boolean filter on source and target ensures only the bounded window is touched — unmatched records outside that window are left alone.

[change-data-feed](change-data-feed/) · [what-is-cdc](what-is-cdc/) · [low-shuffle-merge](low-shuffle-merge/) · [row-tracking](row-tracking/)
