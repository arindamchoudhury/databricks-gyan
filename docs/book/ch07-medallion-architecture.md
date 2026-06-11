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

`CREATE OR REPLACE TABLE AS SELECT` (CRAS) atomically drops and re-creates the table. On each pipeline run, Silver is rebuilt from Bronze — a "full refresh" pattern. This is safe when Bronze is the source of truth and Silver is purely derived.

Functions used here:

| Function | Returns | Notes |
|----------|---------|-------|
| `upper(str)` | STRING | Normalises text casing |
| `current_timestamp()` | TIMESTAMP | UTC timestamp at query execution time |
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

This differs from `CREATE OR REPLACE TABLE`, which would reset the version history. For Gold tables that are monitored by dashboards or downstream jobs, keeping the history is useful for debugging.

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
- **Use INSERT OVERWRITE for Gold** — unlike CRAS, INSERT OVERWRITE preserves the table's Delta history, making it debuggable. If a Gold aggregation produces unexpected results, you can compare the current version against yesterday's with time travel.
- **Name temp views clearly** — prefix with `tmp_` or `view_` to make it obvious they're session-scoped and not persisted. `tmp_roles_summary` vs `roles_gold` is unambiguous.
- **Check lineage before renaming tables** — Unity Catalog lineage is based on table names. If you rename `employees_silver` to `staff_silver`, the lineage graph shows a break. Update downstream dependencies before or alongside any rename.

## Common pitfalls

- **CRAS drops Delta history** — if you're using `CREATE OR REPLACE TABLE` for Silver, the previous versions are gone. If Silver consumers rely on time travel (e.g. for SLA monitoring), use `INSERT OVERWRITE` instead.
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
- `INSERT OVERWRITE` replaces rows while preserving Delta history; `CREATE OR REPLACE TABLE` resets history.
- Unity Catalog tracks table-level (and column-level) lineage automatically — view it in the Catalog Explorer.
- The full pipeline is idempotent: re-running produces the same result without duplicates.

The next chapter covers Auto Loader and incremental ingestion patterns for high-volume, continuous pipelines.
