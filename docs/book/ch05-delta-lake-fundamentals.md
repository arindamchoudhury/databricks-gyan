# Chapter 5: Delta Lake Fundamentals

> **Source:** DA-FREE v3.1.1 — M2-01: Creating and Working with a Delta Table
> **Added:** 2026-06-11

## What you'll learn

- Why all Databricks tables are Delta tables and what that gives you
- How to create a Delta table from a CSV file using `read_files()` and CTAS
- How to inspect a table's schema, storage details, and version history
- How DML operations (INSERT, UPDATE, DELETE) interact with the Delta transaction log
- How to time-travel to any previous table version

## The problem this solves

Traditional data lakes store raw files with no schema enforcement, no ACID guarantees, and no way to undo a bad write. Delta Lake is the storage layer that turns a folder of Parquet files into a reliable, versioned, queryable table. On Databricks, every table you create is a Delta table by default — you get all of this automatically.

## Core concept

A Delta table is a directory of Parquet files plus a `_delta_log/` transaction log. Every write (INSERT, UPDATE, DELETE, MERGE, OPTIMIZE) appends a new JSON entry to the log. This gives you:

- **ACID transactions**: writes are atomic — either all committed or none
- **Versioned history**: every state of the table is preserved and queryable
- **Schema enforcement**: writes that don't match the schema are rejected
- **Time travel**: query any past version by version number or timestamp

Critically, these ACID guarantees hold across **both batch and streaming** writers to the same table — the log is the single point of serialization — so you can append a stream and run a batch `MERGE` against one table without corrupting it. That is precisely what a raw data lake cannot do, and the reason the lakehouse can collapse batch + streaming onto one copy ([Lakehouse-Dummies Ch 3](../sources/lakehouse-dummies/03-underlying-technology/)).

> 💡 **Delta vs. Iceberg.** Delta Lake and Apache Iceberg are the two leading *open* table formats, and both sit on top of plain **Parquet** data files — the difference is the metadata/transaction layer above. Their feature sets are broadly similar; companies pick by ecosystem. Delta is Databricks-native with schema enforcement and built-in lineage. Because both are open, your data avoids vendor lock-in either way, and Databricks **UniForm** lets a Delta table expose Iceberg-compatible metadata so Iceberg readers can query it (Ch 22).

The Unity Catalog namespace gives every table a stable address: `catalog.schema.table`. Tables created without `LOCATION` are **managed tables** — Databricks owns the lifecycle and deletes the underlying files when you `DROP TABLE`. Tables created with `LOCATION` pointing to external storage are **external tables** — dropping the table removes the catalog entry but not the files.

`read_files()` is the recommended SQL function for reading raw files into a query or CTAS. It accepts format options inline and automatically adds a `_rescued_data` column to capture rows that don't fit the inferred schema.

## Code examples

### Setting context

```sql
USE CATALOG my_catalog;
USE SCHEMA my_schema;

SELECT current_catalog(), current_schema();
```

### Reading a file without creating a table

```sql
-- Quick preview — no table created
SELECT * FROM csv.`/Volumes/my_catalog/my_schema/my_volume/employees.csv`;

-- With format options via read_files()
SELECT *
FROM read_files(
  '/Volumes/my_catalog/my_schema/my_volume/',
  format => 'csv',
  header => true,
  inferSchema => true
);
```

### CTAS — create a managed Delta table from CSV

```sql
DROP TABLE IF EXISTS employees;

CREATE TABLE employees AS
SELECT ID, FirstName, Country, Role
FROM read_files(
  '/Volumes/my_catalog/my_schema/my_volume/',
  format => 'csv',
  header => true,
  inferSchema => true
);
```

No `USING DELTA` needed — Delta is the default format. This creates a managed table: the data is stored in Unity Catalog-managed storage.

### Python equivalent

```python
df = (spark.read
      .format("csv")
      .option("header", "true")
      .option("inferSchema", "true")
      .load("/Volumes/my_catalog/my_schema/my_volume/"))

(df.write
   .mode("overwrite")
   .format("delta")
   .saveAsTable("my_catalog.my_schema.employees"))
```

### Inspecting a table

```sql
-- Column names, types, nullability, comments
DESCRIBE employees;

-- Everything above + table metadata: type (Managed/External), provider, location
DESCRIBE EXTENDED employees;

-- Storage details: format, location, numFiles, sizeInBytes, partitionColumns
DESCRIBE DETAIL employees;

-- Full version history: version, timestamp, operation, operationParameters, operationMetrics
DESCRIBE HISTORY employees;
```

### DML operations

Each operation creates a new version in the Delta log:

```sql
-- Version N+1: insert
INSERT INTO employees VALUES
  (5555, 'Alex', 'USA', 'Instructor'),
  (6666, 'Sanjay', 'India', 'Instructor');

-- Version N+2: update
UPDATE employees
  SET Role = 'Senior Manager'
  WHERE ID = 1111;

-- Version N+3: delete
DELETE FROM employees
  WHERE ID = 3333;
```

### Time travel

```sql
-- Query the original table (version 0)
SELECT * FROM employees VERSION AS OF 0;

-- Shorthand
SELECT * FROM employees@v0;

-- By timestamp
SELECT * FROM employees TIMESTAMP AS OF '2026-01-01T00:00:00';
```

Time travel requires that the old Parquet files haven't been vacuumed. By default, `VACUUM` retains files for 7 days (`deletedFileRetentionDuration = interval 7 days`).

> ⚠️ **DBR 18 change:** Databricks now blocks time-travel queries beyond the `deletedFileRetentionDuration` threshold (default 7 days) for *all* tables. DBR 18 also keeps the two retention properties consistent — you can't set `deletedFileRetentionDuration` larger than `logRetentionDuration`, or vice versa. Keep `VACUUM` at the default threshold or higher in production.

## Best practices

- **Use CTAS for initial table creation** — it's atomic (all-or-nothing) and infers schema automatically via `read_files()`. You can always tighten the schema with `ALTER TABLE` later.
- **Use `DESCRIBE DETAIL`** to verify a table's physical location and file count after large writes. Unexpected file counts indicate something went wrong.
- **Rely on Predictive Optimization** for maintenance. It is **on by default** for Unity Catalog managed tables (accounts created on or after 2024-11-11; existing accounts are being enabled in a gradual rollout). Databricks automatically runs `OPTIMIZE` and `VACUUM` in the background, so you get compacted files and controlled history retention without manual maintenance. On older accounts, confirm it's active rather than assuming you need to enable it.
- **Prefer managed tables** for most data engineering work. External tables are appropriate when another system (e.g. an existing Hive metastore) already owns the data lifecycle.
- **Don't run `VACUUM` with retention < 7 days** in production. Shorter retention breaks time travel and can interfere with concurrent readers.

## Common pitfalls

- **`_rescued_data` column** appears in `read_files()` output. It contains JSON for rows where a column value couldn't be parsed into the inferred type. Don't ignore it — non-null entries signal data quality issues in the source.
- **Predictive Optimization creates extra versions**: `DESCRIBE HISTORY` may show `OPTIMIZE` operations you didn't trigger. This is expected — predictive optimization runs automatically. The versions are safe to ignore.
- **Direct file queries (`csv.\`/path/\``) don't treat the first row as a header** by default. You get headers as data. Always use `read_files()` with `header => true` for structured files.
- **Forgetting `USE CATALOG`/`USE SCHEMA`** means your `CREATE TABLE` lands in the wrong schema. Confirm with `SELECT current_catalog(), current_schema()` before any DDL.
- **`CREATE OR REPLACE TABLE` vs `DROP` + `CREATE`** — these are not equivalent. `CREATE OR REPLACE TABLE` (REPLACE) is atomic and **preserves history**: the versions before and after the replace both stay in the transaction log, so you can still time-travel or `RESTORE` to a pre-replace version (column masks on surviving columns are kept too). It replaces the data and resets table properties to those declared in the statement. What actually destroys history is `DROP TABLE` followed by `CREATE TABLE` — that removes the table from the metastore and starts a fresh log. For routine updates, prefer `INSERT OVERWRITE` or `MERGE`.

## Exercises

1. **Recall** — What is stored in the `_delta_log/` directory, and what does each new entry represent?
2. **Apply** — Create a CSV file with 5 rows, upload it to a Unity Catalog Volume, create a Delta table from it using `read_files()`, update one row, delete one row, and then query the original version using time travel.
3. **Extend** — Run `DESCRIBE HISTORY` on a table after several DML operations. Find the operation that has the highest `numOutputRows` in its `operationMetrics`. What can you infer about the data flow?

## Summary

- Delta Lake adds ACID transactions, versioned history, and schema enforcement to Parquet files.
- All Databricks tables are Delta tables by default — no extra configuration needed.
- `read_files()` is the SQL TVF for reading raw files with format options; use it inside CTAS.
- Every DML operation appends a new version to the transaction log, enabling time travel.
- `DESCRIBE DETAIL` and `DESCRIBE HISTORY` are your primary inspection commands.
- Delta and Iceberg are the two open table formats over Parquet; ACID holds across batch *and* streaming writers, which is what lets one table serve both.

## References

- [The Data Lakehouse For Dummies — Ch 3 (Kaplan & Kara, 2026)](../sources/lakehouse-dummies/03-underlying-technology/) — open storage formats (Delta vs. Iceberg on Parquet), ACID across batch + streaming, and Unity Catalog governance (reading notes).

The next chapter covers the different ways to ingest data into Delta tables: CTAS, COPY INTO, and Auto Loader.
