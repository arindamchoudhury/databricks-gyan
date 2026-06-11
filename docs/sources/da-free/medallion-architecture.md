# M2-03: Transforming Data Using the Medallion Architecture

> **Source:** DA-FREE v3.1.1 — `M2 - Using Databricks for Data Engineering/DEWD00 - 03-Transforming Data Using the Medallion Architecture.ipynb`
> **Added:** 2026-06-11
> **Tags:** medallion, bronze, silver, gold, lineage, unity-catalog, B7
> **Type:** notebook

> 📌 **Full explained chapter:** [[ch07-medallion-architecture]]

## Summary

Builds a three-layer Medallion pipeline end-to-end in a single notebook: Bronze (raw CSV ingestion via COPY INTO), Silver (enriched Delta table with transformations), Gold (aggregated table via INSERT OVERWRITE from a temp view). Also covers Unity Catalog lineage via Catalog Explorer.

## Key points

- **Bronze**: raw data landed unchanged from source files via COPY INTO.
- **Silver**: cleaned, enriched — transformations applied (uppercase, timestamp columns added).
- **Gold**: business-level aggregation — total employees by role via GROUP BY.
- `CREATE OR REPLACE TABLE AS SELECT` re-creates the Silver table on each run.
- `CREATE OR REPLACE TEMP VIEW` + `INSERT OVERWRITE TABLE` pattern for Gold.
- Unity Catalog automatically tracks lineage: Gold table shows Silver as upstream source.
- The Catalog Explorer **Lineage** tab visualises the full dependency graph.

## Notes

### Bronze — COPY INTO from volume

```sql
DROP TABLE IF EXISTS current_employees_bronze;

CREATE TABLE IF NOT EXISTS current_employees_bronze (
  ID INT,
  FirstName STRING,
  Country STRING,
  Role STRING
);
```

```python
spark.sql(f'''
  COPY INTO current_employees_bronze
  FROM '/Volumes/dbacademy/{DA.schema_name}/myfiles/'
  FILEFORMAT = CSV
  FORMAT_OPTIONS (
    'header' = 'true',
    'inferSchema' = 'true'
  )
''').display()
```

Bronze tables preserve source data exactly. No transformations here.

### Silver — transform and enrich

```sql
CREATE OR REPLACE TABLE current_employees_silver AS
SELECT
  ID,
  FirstName,
  Country,
  upper(Role) AS Role,                         -- normalise casing
  current_timestamp() AS CurrentTimeStamp,      -- audit column
  date(CurrentTimeStamp) AS CurrentDate         -- derived date
FROM current_employees_bronze;
```

`CREATE OR REPLACE TABLE AS SELECT` (CRAS) atomically re-creates the table. Good for batch refreshes where you want to replace the entire Silver layer from Bronze on each run.

Functions used:

| Function | Returns |
|----------|---------|
| `upper(col)` | string in ALL CAPS |
| `current_timestamp()` | current datetime as TIMESTAMP |
| `date(timestamp)` | DATE extracted from TIMESTAMP |

### Gold — aggregate with temp view + INSERT OVERWRITE

```sql
-- Step 1: aggregate into a temp view
CREATE OR REPLACE TEMP VIEW temp_view_total_roles AS
SELECT
  Role,
  count(*) AS TotalEmployees
FROM current_employees_silver
GROUP BY Role;

-- Step 2: persist the target table (once)
CREATE TABLE IF NOT EXISTS total_roles_gold (
  Role STRING,
  TotalEmployees INT
);

-- Step 3: overwrite with fresh aggregation on each run
INSERT OVERWRITE TABLE total_roles_gold
SELECT * FROM temp_view_total_roles;
```

`INSERT OVERWRITE` replaces all rows in the table but keeps the table definition and properties (unlike `DROP + CREATE`). Creates a new Delta version on each run.

Temp views exist only for the current notebook session — they are not persisted to the catalog.

### Unity Catalog lineage

After running the pipeline, lineage is automatically tracked:

```
Catalog Explorer → total_roles_gold → Lineage tab
→ shows current_employees_silver as upstream dependency
→ "See lineage graph" for visual DAG
```

Lineage is tracked at the column level when running via Spark on DBR 13.3+.

### Catalog Explorer: Permissions, History, Insights

- **Permissions** tab: `GRANT` / `REVOKE` privileges on the table
- **History** tab: Delta version history (same as `DESCRIBE HISTORY`)
- **Insights** tab: frequent queries and users in the last 30 days

## Related sources

- [[ingesting-data]] — COPY INTO idempotency details
- [[creating-delta-table]] — Delta table fundamentals
- [[ch07-medallion-architecture]] — full explanatory chapter
