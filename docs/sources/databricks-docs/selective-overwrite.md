# Selectively overwrite data with Delta Lake

> **Source:** [docs.databricks.com/aws/en/delta/selective-overwrite](https://docs.databricks.com/aws/en/delta/selective-overwrite)
> **Added:** 2026-06-29
> **Source updated:** 2026-05-11
> **Tags:** delta, overwrite, replace-where, replace-using, replace-on, dynamic-partition-overwrite, selective-overwrite, I5, I1
> **Type:** documentation

Four options for selective overwrites — replacing a subset of rows without touching the rest:

| Option | Use case | Compute | Min version |
|---|---|---|---|
| `REPLACE WHERE` | Overwrite rows matching a **predicate** | All | SQL: DBR 12.2 LTS+; Python/Scala: DBR 9.1 LTS+ |
| `REPLACE USING` | Dynamic overwrite: replace rows where **specified columns compare equal** | All | SQL: DBR 16.3+; Python/Scala: DBR 18.2+ |
| `REPLACE ON` | Dynamic overwrite by **boolean expression** (NULL-safe `<=>` etc.) | All | SQL: DBR 17.1+; Python/Scala: DBR 18.2+ |
| `partitionOverwriteMode` | **Legacy** dynamic partition overwrite — replaces every partition touched | SQL: classic only; Python/Scala: all | DBR 11.3 LTS+ |

**Recommendation:** use `REPLACE USING` or `REPLACE WHERE` for most cases. Use `REPLACE ON` only when you need NULL-safe or complex matching. `partitionOverwriteMode` is legacy — prefer `REPLACE USING`.

`replaceOn` and `replaceUsing` cannot be combined with `replaceWhere`, `partitionOverwriteMode`, or `overwriteSchema` in Python/Scala. For accidentally overwritten data, use `restore`.

## REPLACE WHERE

Atomically overwrite all rows matching an arbitrary predicate. All written rows must satisfy the predicate (validated by default).

```sql
INSERT INTO TABLE events
  REPLACE WHERE start_date >= '2017-01-01' AND end_date <= '2017-01-31'
  SELECT * FROM replace_data
```

```python
(replace_data.write
  .mode("overwrite")
  .option("replaceWhere", "start_date >= '2017-01-01' AND end_date <= '2017-01-31'")
  .saveAsTable("events")
)
```

**Constraint check (default on):** if any row in the write falls outside the predicate, the operation fails. Disable on classic compute only:

```python
spark.conf.set("spark.databricks.delta.replaceWhere.constraintCheck.enabled", False)
```

**Beta:** for incremental refresh use `REPLACE WHERE` flows in Spark Declarative Pipelines (SDP).

**Empty source:** `REPLACE WHERE` **may delete** rows in the predicate range (unlike `REPLACE USING`/`REPLACE ON`).

**Legacy behavior (classic only):** predicate applied over partition columns only. Disable the new behavior to use it: `spark.databricks.delta.replaceWhere.dataColumns.enabled = false`.

## REPLACE USING

Dynamic data overwrite — replaces rows where the specified columns compare **equal**. Works on partitioned, unpartitioned, and liquid-clustered tables. No session configuration needed; compute-independent.

```sql
INSERT INTO TABLE events
  REPLACE USING (event_id, start_date)
  SELECT * FROM source_data
```

```python
(sourceDataDF.write
  .mode("overwrite")
  .option("replaceUsing", "event_id, start_date")
  .saveAsTable("events")
)
```

Empty source → **no rows deleted**.

**Legacy (DBR 16.3–17.1):** only partition columns allowed in `USING`; DBR 17.2+ allows any columns.

## REPLACE ON

Like `REPLACE USING` but with a **user-defined boolean expression** — use when you need NULL-safe equality (`<=>`) or complex conditions.

```sql
INSERT INTO TABLE events AS t
  REPLACE ON (s.event_id <=> t.event_id AND s.start_date <=> t.start_date)
  (SELECT * FROM source_data) AS s
```

```python
(sourceDataDF.alias("s")
  .write
  .mode("overwrite")
  .option("targetAlias", "t")
  .option("replaceOn", "s.event_id <=> t.event_id AND s.start_date <=> t.start_date")
  .saveAsTable("events")
)
```

Empty source → **no rows deleted**.

## partitionOverwriteMode (legacy)

Replaces **every partition** that the write touches; leaves other partitions unchanged. Classic compute only for SQL; Python/Scala supports all compute.

```sql
SET spark.sql.sources.partitionOverwriteMode=dynamic;
INSERT OVERWRITE TABLE default.people10m SELECT * FROM morePeople;
```

```python
(df.write
  .mode("overwrite")
  .option("partitionOverwriteMode", "dynamic")
  .saveAsTable("default.people10m")
)
```

Constraints: can't combine with `overwriteSchema=true`; can't combine `replaceWhere` and `partitionOverwriteMode` in the same `DataFrameWriter` call. A single row landing in the wrong partition silently overwrites that entire partition.

[merge](merge/) · [schema-evolution](schema-evolution/) · [change-data-feed](change-data-feed/)
