# Chapter 6: Data Ingestion Basics

> **Source:** DA-FREE v3.1.1 — M2-02: Ingesting Data into Delta Lake
> **Added:** 2026-06-11

## What you'll learn

- When to use CTAS vs COPY INTO vs Auto Loader for ingesting files into Delta tables
- How COPY INTO achieves idempotency and why that matters
- How to upload files manually via the Catalog Explorer UI
- How to list volume contents from Python and SQL
- The conceptual difference between batch ingestion and streaming ingestion

## The problem this solves

Data lands in cloud storage (S3, ADLS, GCS) as files — CSV, JSON, Parquet, Avro. You need to get those files into a Delta table reliably. "Reliably" means: no duplicates when the pipeline re-runs, no missed files, no data loss. COPY INTO solves this for batch ingestion by tracking which files have been loaded. Auto Loader solves it for streaming ingestion by using cloud storage notifications.

## Core concept

Three ingestion patterns, each suited to a different scenario:

| Pattern | How it works | Best for |
|---------|-------------|---------|
| **CTAS** (`CREATE TABLE AS SELECT`) | One-shot full load from a path | Initial load of a static dataset |
| **COPY INTO** | Tracks loaded files in the Delta log; only loads new files on re-runs | Incremental batch ingestion; scheduled jobs |
| **Auto Loader** (`cloudFiles` format) | Streaming; detects new files via cloud notifications or listing | High-volume, continuous ingestion |

**COPY INTO idempotency** is the key property that makes it production-safe. Internally, COPY INTO stores a set of file paths that have already been loaded inside the Delta transaction log. On each run, it checks new files in the source path against this set and skips any that are already there. This means running COPY INTO twice on the same source produces exactly the same result as running it once — no duplicates.

```
Run 1: employees.csv → 4 rows loaded
Run 2: employees.csv → 0 rows loaded (already tracked)
Run 3: employees.csv + employees2.csv → 2 rows loaded (only the new file)
```

**Auto Loader** extends this to streaming: instead of polling a path, it subscribes to cloud storage change notifications (or uses incremental directory listing as a fallback). Each new file is processed exactly once, tracked by a checkpoint. Auto Loader scales to millions of files where COPY INTO starts to show checkpoint overhead.

## Code examples

### CTAS — one-shot full load

```sql
CREATE TABLE employees AS
SELECT *
FROM read_files(
  '/Volumes/my_catalog/my_schema/my_volume/',
  format => 'csv',
  header => true,
  inferSchema => true
);
```

Suitable for initial loads. Not suitable for incremental appends — re-running replaces all data.

### COPY INTO — incremental idempotent batch load

```sql
-- Step 1: create the target table first (COPY INTO requires an existing table)
CREATE TABLE IF NOT EXISTS employees_incremental (
  ID INT,
  FirstName STRING,
  Country STRING,
  Role STRING
);

-- Step 2: load files (safe to re-run)
COPY INTO employees_incremental
FROM '/Volumes/my_catalog/my_schema/my_volume/'
FILEFORMAT = CSV
FORMAT_OPTIONS (
  'header' = 'true',
  'inferSchema' = 'true'
);
```

The return value contains `num_affected_rows`, `num_inserted_rows`, `num_skipped_corrupt_files`. When `num_inserted_rows = 0`, no new files were found.

In Python (when you need to interpolate a variable path):

```python
result = spark.sql(f'''
  COPY INTO my_catalog.my_schema.employees_incremental
  FROM '/Volumes/my_catalog/{schema_name}/my_volume/'
  FILEFORMAT = CSV
  FORMAT_OPTIONS (
    'header' = 'true',
    'inferSchema' = 'true'
  )
''')
result.display()
```

### Listing volume contents

```python
# Python: dbutils
files = dbutils.fs.ls('/Volumes/my_catalog/my_schema/my_volume/')
display(files)
```

```sql
-- SQL
LIST '/Volumes/my_catalog/my_schema/my_volume/';
```

Both return file name, size, and modification time.

### Upload UI — no code needed

For one-off loads of small files without writing any code:

```
Catalog Explorer → your schema → Create → Table
→ Upload file (drag-and-drop or browse)
→ Set table name and catalog/schema
→ Create table
```

Databricks infers the schema from the file and creates a managed Delta table.

### Auto Loader — conceptual pattern

```python
(spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "csv")
  .option("cloudFiles.schemaLocation", "/Volumes/catalog/schema/volume/_schema")
  .load("/Volumes/catalog/schema/volume/")
  .writeStream
  .option("checkpointLocation", "/Volumes/catalog/schema/volume/_checkpoint")
  .toTable("my_catalog.my_schema.employees_streaming"))
```

Key differences from COPY INTO:
- **Continuous**: processes files as they arrive, not on a triggered schedule
- **Checkpoint-based**: tracks progress via a checkpoint directory, not the Delta log
- **Scales to millions of files**: efficient for high-volume ingestion pipelines
- **Schema evolution**: `cloudFiles.inferColumnTypes` and `cloudFiles.schemaEvolutionMode` handle schema changes automatically

> ⚠️ **DBR 17.3 breaking change:** `input_file_name()` — previously used to capture the source file name per row — was removed. Use `df.select("_metadata.file_name")` instead. The `_metadata` struct is available on all file-based DataFrames and contains `file_name`, `file_path`, `file_size`, `file_modification_time`.

## Best practices

- **COPY INTO for scheduled batch jobs** — create the table once, then let COPY INTO manage incremental loads. Pair it with a Lakeflow Job on a schedule.
- **Auto Loader for continuous pipelines** — if files arrive frequently or at high volume, streaming with Auto Loader avoids the polling overhead of COPY INTO.
- **Don't use CTAS in incremental pipelines** — CTAS is a full replacement, not an append. Every re-run overwrites the table.
- **Always create the target table before COPY INTO** — the table must exist. Use `CREATE TABLE IF NOT EXISTS` with the expected schema to make the pipeline idempotent on first run.
- **Store checkpoints and schema locations in Volumes** — use Unity Catalog Volumes for Auto Loader checkpoint and schema directories. They're governed, discoverable, and backed by your cloud storage.

## Common pitfalls

- **COPY INTO doesn't auto-create the target table** — if the table doesn't exist, COPY INTO fails with a "table not found" error. Always pre-create with `CREATE TABLE IF NOT EXISTS`.
- **Mixing COPY INTO and other writes** — COPY INTO tracks files at the table level. If you also write to the table via other operations (INSERT, MERGE), the file tracking is independent of those rows. The duplicate-prevention only covers files loaded by COPY INTO, not rows inserted by other means.
- **Auto Loader schema hints vs inference** — by default, Auto Loader infers all columns as strings when `cloudFiles.inferColumnTypes` is false (the default). Set it to `true` or provide an explicit schema to avoid downstream casting.
- **Large volumes with COPY INTO** — COPY INTO stores loaded file paths in the Delta log checkpoint. With millions of small files, this checkpoint can grow large. Prefer Auto Loader with directory listing for very high file counts.
- **Upload UI for production** — the Catalog Explorer upload UI is for exploration only. Don't use it in production pipelines — use COPY INTO or Auto Loader instead.

## Exercises

1. **Recall** — Where does COPY INTO store its record of which files have been loaded? What happens if you `DROP TABLE` and recreate the table?
2. **Apply** — Create a Delta table, load a CSV file into it with COPY INTO, verify the row count, then upload a second CSV file to the same volume path and run COPY INTO again. Confirm that only the new rows are added.
3. **Extend** — Design an ingestion pipeline for a scenario where new CSV files arrive every hour in a Volume. Should you use COPY INTO or Auto Loader? Write out the trade-offs and the code for your chosen approach.

## Summary

- CTAS is a one-shot full load — not suitable for incremental pipelines.
- COPY INTO tracks loaded files in the Delta log, making re-runs safe and idempotent.
- Auto Loader extends COPY INTO's pattern to streaming, scaling to millions of files.
- `_metadata.file_name` replaces the removed `input_file_name()` function (DBR 17.3+).
- Always pre-create the target table before running COPY INTO.

The next chapter shows how to chain Bronze → Silver → Gold transformations into a full Medallion Architecture pipeline.
