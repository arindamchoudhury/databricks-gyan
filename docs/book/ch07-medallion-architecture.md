# Chapter 7: Medallion Architecture

> **Source:** DA-FREE v3.1.1 — M2-03: Transforming Data Using the Medallion Architecture
> **Added:** 2026-06-11

## What you'll learn

- What the Bronze / Silver / Gold layers are and why they exist
- How to implement each layer in SQL using Delta tables
- The difference between `CREATE OR REPLACE TABLE AS SELECT` and `INSERT OVERWRITE`
- How Unity Catalog tracks data lineage automatically across layers
- How to view the lineage graph in the Catalog Explorer

## The problem this solves

Raw data is messy: inconsistent casing, missing audit trails, no aggregations. Analysts need clean, aggregated data; but data engineers also need to preserve the raw source for debugging, reprocessing, and compliance. The Medallion Architecture solves this by separating concerns into three layers: raw (Bronze), cleaned (Silver), and aggregated (Gold). Each layer serves different consumers without destroying the original data.

## Core concept

The Medallion Architecture is a data design pattern that organises a data lake into three progressively refined layers:

```
Source Files
    ↓  COPY INTO (idempotent, incremental)
[ Bronze ]  — raw, unchanged, append-only
    ↓  CRAS (CREATE OR REPLACE AS SELECT)
[ Silver ]  — cleaned, typed, enriched
    ↓  TEMP VIEW + INSERT OVERWRITE
[ Gold ]    — aggregated, business-ready
```

**Bronze** is an exact copy of source data. No transformations. The goal is to land data reliably and reproducibly — if anything goes wrong downstream, you can always reprocess from Bronze.

**Silver** applies cleaning transformations: normalise casing, parse types, add audit columns (load timestamp, source file name). Silver tables are typically the join layer — they're clean enough to query but retain full row-level detail.

**Gold** aggregates and summarises. Gold tables are designed for specific business queries: totals by role, daily revenue by region, weekly active users. They're small, fast, and optimised for dashboard consumption.

The three-layer pattern maps naturally to different write patterns:

| Layer | Write pattern | Rationale |
|-------|--------------|-----------|
| Bronze | COPY INTO (append) | Idempotent, incremental; never lose raw data |
| Silver | CREATE OR REPLACE TABLE AS SELECT | Atomic full refresh from Bronze on each run |
| Gold | INSERT OVERWRITE from TEMP VIEW | Replace aggregation results; keep table definition |

## Code examples

### Bronze — COPY INTO from Volume

```sql
CREATE TABLE IF NOT EXISTS employees_bronze (
  ID INT,
  FirstName STRING,
  Country STRING,
  Role STRING
);
```

```python
spark.sql(f'''
  COPY INTO employees_bronze
  FROM '/Volumes/my_catalog/{schema_name}/myfiles/'
  FILEFORMAT = CSV
  FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
''').display()
```

Run this as often as new files arrive. Already-loaded files are skipped automatically.

### Silver — transform with CRAS

```sql
CREATE OR REPLACE TABLE employees_silver AS
SELECT
  ID,
  FirstName,
  Country,
  upper(Role)          AS Role,
  current_timestamp()  AS LoadTimestamp,
  date(LoadTimestamp)  AS LoadDate
FROM employees_bronze;
```

`CREATE OR REPLACE TABLE AS SELECT` (CRAS) atomically **replaces the table's contents** — it does *not* drop the table. The replace is a single new commit appended to the same `_delta_log/`, so the table identity and its full version history are retained (you can still time-travel to versions before the replace). On each pipeline run, Silver is rebuilt from Bronze — a "full refresh" pattern. This is safe when Bronze is the source of truth and Silver is purely derived.

Functions used here:

| Function | Returns | Notes |
|----------|---------|-------|
| `upper(str)` | STRING | Normalises text casing |
| `current_timestamp()` | TIMESTAMP | Timestamp at query start, in the session timezone (`spark.sql.session.timeZone`) — UTC by default on Databricks |
| `date(timestamp)` | DATE | Extracts the date part |

### Gold — aggregate with TEMP VIEW + INSERT OVERWRITE

```sql
-- Step 1: define the aggregation as a temp view (session-scoped, not persisted)
CREATE OR REPLACE TEMP VIEW roles_summary AS
SELECT
  Role,
  count(*) AS TotalEmployees
FROM employees_silver
GROUP BY Role;

-- Step 2: create the target table once (schema stays fixed)
CREATE TABLE IF NOT EXISTS roles_gold (
  Role         STRING,
  TotalEmployees INT
);

-- Step 3: overwrite data on each run (keeps table definition and properties)
INSERT OVERWRITE TABLE roles_gold
SELECT * FROM roles_summary;
```

`INSERT OVERWRITE` replaces all rows but keeps the table's schema, properties, and Delta version history. A new Delta version is written on each run — you can time-travel to any previous aggregation state.

Both `INSERT OVERWRITE` and `CREATE OR REPLACE TABLE` preserve Delta history, so either gives you time travel. The real difference is **schema control**: `INSERT OVERWRITE` writes into the table's pre-declared, fixed schema, whereas CRAS derives a fresh schema from its `SELECT` each run. For a Gold table whose shape is a stable contract consumed by dashboards and downstream jobs, `INSERT OVERWRITE` into a fixed schema is the safer choice — an accidental change to the aggregation query can't silently reshape the table.

### Verifying lineage in Catalog Explorer

After running the pipeline:

```
Catalog Explorer → roles_gold → Lineage tab
→ See employees_silver listed as an upstream source
→ "See lineage graph" → visual DAG of the full pipeline
```

Unity Catalog tracks lineage automatically at the table level (and column level on DBR 13.3+). No annotations needed — every read from `employees_silver` while writing `roles_gold` is captured.

### Full pipeline in sequence

```sql
-- 1. Bronze
COPY INTO employees_bronze FROM '/Volumes/...' FILEFORMAT = CSV ...;

-- 2. Silver
CREATE OR REPLACE TABLE employees_silver AS
SELECT ID, FirstName, Country, upper(Role) AS Role,
       current_timestamp() AS LoadTimestamp, date(LoadTimestamp) AS LoadDate
FROM employees_bronze;

-- 3. Gold
CREATE OR REPLACE TEMP VIEW roles_summary AS
SELECT Role, count(*) AS TotalEmployees FROM employees_silver GROUP BY Role;

INSERT OVERWRITE TABLE roles_gold SELECT * FROM roles_summary;
```

This is idempotent: re-running produces the same result.

## Best practices

- **Keep Bronze immutable** — never update or delete from Bronze. It's your source of truth for reprocessing. If a source system sends corrections, land them as new rows with a version or sequence column, and handle them in Silver.
- **Use CRAS for Silver full refreshes** — when Silver is fully derived from Bronze, CRAS is the simplest and most atomic pattern. It handles schema changes automatically (the new schema comes from the SELECT).
- **Use INSERT OVERWRITE for Gold** — it writes into a fixed, pre-declared schema, so an accidental change to the aggregation query can't silently reshape a table that dashboards depend on. (Both INSERT OVERWRITE and CRAS preserve Delta history, so you get time travel either way — you can still compare today's aggregation against yesterday's to debug unexpected results.)
- **Name temp views clearly** — prefix with `tmp_` or `view_` to make it obvious they're session-scoped and not persisted. `tmp_roles_summary` vs `roles_gold` is unambiguous.
- **Check lineage before renaming tables** — Unity Catalog lineage is based on table names. If you rename `employees_silver` to `staff_silver`, the lineage graph shows a break. Update downstream dependencies before or alongside any rename.

## Common pitfalls

- **`DROP TABLE` + `CREATE TABLE` destroys history — CRAS does not.** A common misconception is that `CREATE OR REPLACE TABLE` (CRAS) loses history. It doesn't: REPLACE appends a new commit to the same transaction log, so prior versions remain queryable. What actually wipes history is dropping the table and recreating it — `DROP TABLE` deletes the `_delta_log/` (for managed tables, the whole directory), and the new table starts fresh at version 0. If you need a clean refresh of Silver, prefer CRAS over DROP+CREATE precisely so consumers keep time travel.
- **Temp views don't survive session end** — if a job runs in a new session, a temp view from a previous session is gone. Don't rely on temp views being available across job runs. Create them fresh each time they're needed, or use permanent views for shared intermediate results.
- **Gold tables read by dashboards can have stale data** — if Gold is populated by a scheduled job and a dashboard queries it during the INSERT OVERWRITE, the query may read an empty or partially populated table. Consider using Delta's `MERGE` or writing to a staging table and atomically swapping.
- **Forgetting to create the Gold table** before `INSERT OVERWRITE` — the table must exist. `CREATE TABLE IF NOT EXISTS` is the right guard; `INSERT OVERWRITE` will fail if the table doesn't exist.
- **Lineage gaps from Python writes** — `df.write.saveAsTable()` in Python is tracked by Unity Catalog. But writes via `df.write.save("/path/")` to a path (not a table) are not tracked. Use `saveAsTable()` for all writes that should appear in the lineage graph.

## Exercises

1. **Recall** — What is the difference between `CREATE OR REPLACE TABLE AS SELECT` and `INSERT OVERWRITE TABLE`? When would you choose one over the other for a Silver vs Gold layer?
2. **Apply** — Implement the full Bronze → Silver → Gold pipeline from scratch for a new dataset (you can use any CSV file). After running it, open the Catalog Explorer and verify the lineage graph shows all three tables connected.
3. **Extend** — Add a fourth "Platinum" layer that joins `roles_gold` with a `departments` table to produce a report of employee counts by department and role. What write pattern would you use for the Platinum layer, and why?

## Summary

- Bronze = raw data, append-only via COPY INTO; Silver = cleaned via CRAS; Gold = aggregated via INSERT OVERWRITE.
- `upper()`, `current_timestamp()`, and `date()` are the key transformation functions in the Silver layer.
- Both `INSERT OVERWRITE` and `CREATE OR REPLACE TABLE` preserve Delta history (REPLACE appends a commit to the same log); only `DROP` + `CREATE` loses it. Choose INSERT OVERWRITE for Gold to lock the schema, CRAS for Silver to let the schema follow the SELECT.
- Unity Catalog tracks table-level (and column-level) lineage automatically — view it in the Catalog Explorer.
- The full pipeline is idempotent: re-running produces the same result without duplicates.

The next chapter covers Auto Loader and incremental ingestion patterns for high-volume, continuous pipelines.
