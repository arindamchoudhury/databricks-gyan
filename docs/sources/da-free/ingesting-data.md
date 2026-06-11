# M2-02: Ingesting Data into Delta Lake

> **Source:** DA-FREE v3.1.1 — `M2 - Using Databricks for Data Engineering/DEWD00 - 02-Ingesting Data into Delta Lake.ipynb`
> **Added:** 2026-06-11
> **Tags:** ingestion, COPY-INTO, CTAS, auto-loader, idempotency, B6
> **Type:** notebook

> 📌 **Full explained chapter:** [[ch06-data-ingestion-basics]]

## Summary

Demonstrates three Delta Lake ingestion techniques side-by-side: CTAS (one-shot full load), Upload UI (manual file upload via Catalog Explorer), and COPY INTO (incremental, idempotent). Includes a live demonstration of COPY INTO's idempotency: running it twice on the same files loads 0 extra rows; only new files are picked up on subsequent runs. Auto Loader is introduced conceptually but not demonstrated hands-on.

## Key points

- **CTAS** — one-shot full load, no incremental tracking.
- **COPY INTO** — tracks which files have been loaded; idempotent; only new files are loaded on re-runs.
- **Upload UI** — Catalog Explorer → Create → Table → upload a local file → create a Delta table without code.
- **Auto Loader** — streaming ingestion that detects new files automatically; outside scope of this course.
- `dbutils.fs.ls()` lists files in a volume (Python utility, not SQL).

## Notes

### COPY INTO — syntax and behaviour

```python
# COPY INTO via Python f-string (to interpolate schema_name)
spark.sql(f'''
COPY INTO current_employees_copyinto
  FROM '/Volumes/dbacademy/{DA.schema_name}/myfiles/'
  FILEFORMAT = CSV
  FORMAT_OPTIONS (
    'header' = 'true',
    'inferSchema' = 'true'
  )
''').display()
```

**Return columns:** `num_affected_rows`, `num_inserted_rows`, `num_skipped_correct_files`

**Idempotency demo:**

| Run | Files in volume | `num_inserted_rows` |
|-----|----------------|---------------------|
| 1st | employees.csv | 4 |
| 2nd (same files) | employees.csv | 0 |
| 3rd (new file added) | employees.csv + employees2.csv | 2 |

COPY INTO tracks file state in the Delta transaction log. Re-running never duplicates data. Only genuinely new files (employees2.csv) are loaded.

### Creating an empty table first

COPY INTO requires the target table to exist. Options:

```sql
-- Option A: define schema explicitly
CREATE TABLE current_employees_copyinto (
  ID INT,
  FirstName STRING,
  Country STRING,
  Role STRING
);

-- Option B: create empty table, let COPY INTO evolve the schema
CREATE TABLE current_employees_copyinto;
```

### Upload UI path

```
Catalog Explorer → your schema → Create (dropdown) → Table
→ upload employees.csv → set table name → Create table
```

Useful for one-off loads of small files. Not suitable for automation.

### Listing volume contents

```python
# Using dbutils (Python only)
files = dbutils.fs.ls(f'/Volumes/dbacademy/{DA.schema_name}/myfiles')
display(files)

# Using SQL
spark.sql(f"LIST '/Volumes/dbacademy/{DA.schema_name}/myfiles/'").display()
```

### Auto Loader — conceptual overview

```python
# Pattern (not demonstrated in this course)
(spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "csv")
  .option("cloudFiles.schemaLocation", "/path/to/schema")
  .load("/Volumes/catalog/schema/volume/")
  .writeStream
  .option("checkpointLocation", "/path/to/checkpoint")
  .toTable("target_table"))
```

Key benefits over COPY INTO:
- Streaming-based (continuous, not triggered)
- No file-state management needed — uses cloud notifications or directory listing
- Scales to millions of files

> ⚠️ **DBR 17.3 breaking change:** `input_file_name()` function removed. Use `df.select("_metadata.file_name")` instead.

## Related sources

- [[creating-delta-table]] — CTAS and read_files basics
- [[medallion-architecture]] — uses COPY INTO for Bronze ingestion
- [[ch06-data-ingestion-basics]] — full explanatory chapter
