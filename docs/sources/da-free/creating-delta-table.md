# M2-01: Creating and Working with a Delta Table

> **Source:** DA-FREE v3.1.1 — `M2 - Using Databricks for Data Engineering/DEWD00 - 01-Creating and Working with a Delta Table.ipynb`
> **Added:** 2026-06-11
> **Tags:** delta-lake, CTAS, read_files, DML, time-travel, unity-catalog, B5
> **Type:** notebook

> 📌 **Full explained chapter:** [[ch05-delta-lake-fundamentals]]

## Summary

Introduces the Unity Catalog object model, then walks through creating a Delta table from a CSV file using both SQL (`CTAS` + `read_files()`) and Python (`spark.read`/`spark.write`). Covers DML operations (INSERT, UPDATE, DELETE), DESCRIBE commands, and Delta time travel.

## Key points

- All saved tables on Databricks are Delta tables by default.
- Unity Catalog uses a three-level namespace: `catalog.schema.table`.
- `USE CATALOG` / `USE SCHEMA` set defaults to avoid fully-qualified names.
- The `IDENTIFIER` clause interprets a string variable as a schema/table/catalog name.
- `read_files()` is a SQL table-valued function for reading files with options (format, header, inferSchema).
- Direct file query syntax: `SELECT * FROM csv.\`/path/to/file\``
- Each DML operation (INSERT, UPDATE, DELETE) creates a new Delta table version.
- Time travel: `VERSION AS OF n` or `@vN` syntax.
- `DESCRIBE DETAIL` shows format, location, file stats. `DESCRIBE HISTORY` shows all versions.
- **Predictive optimization** may auto-run `OPTIMIZE` in the background (shows as a version in history).

## Notes

### Unity Catalog object model

```
Metastore
└── Catalog  (e.g. dbacademy)
    └── Schema / Database  (e.g. labuser_xyz)
        ├── Tables
        ├── Views
        ├── Volumes
        ├── Models
        └── Functions
```

Volumes path format: `/Volumes/catalog_name/schema_name/volume_name/`

### Setting default catalog and schema

**SQL**

```sql
USE CATALOG dbacademy;
USE SCHEMA IDENTIFIER(DA.schema_name);  -- DA.schema_name is a SQL variable (string)

SELECT current_catalog(), current_schema();
```

`IDENTIFIER(expr)` interprets a constant string as a named object — useful when the name is stored in a variable. Avoids quoting issues.

**PySpark** (Spark 3.4+)

```python
spark.catalog.setCurrentCatalog("dbacademy")
spark.catalog.setCurrentDatabase(DA.schema_name)
```

### Exploring a schema

```sql
DESCRIBE SCHEMA EXTENDED IDENTIFIER(DA.schema_name);
SHOW TABLES;
SHOW VOLUMES;
```

```python
# List files in a volume
spark.sql(f"LIST '/Volumes/dbacademy/{DA.schema_name}/myfiles'").display()

# List tables
spark.catalog.listTables(f"dbacademy.{DA.schema_name}")
```

### Reading files directly (without creating a table)

```sql
-- Read CSV as-is (headers become first data row)
SELECT * FROM csv.`/Volumes/dbacademy/schema/myfiles/`;

-- Read as raw text (each line is one string column)
SELECT * FROM text.`/Volumes/dbacademy/schema/myfiles/`;
```

### read_files() — SQL table-valued function

```sql
SELECT *
FROM read_files(
  '/Volumes/dbacademy/' || DA.schema_name || '/myfiles/',
  format => 'csv',
  header => true,
  inferSchema => true
);
```

A `_rescued_data` column is automatically added to capture any rows that don't match the inferred schema.

### CTAS — Create Table As Select

```sql
DROP TABLE IF EXISTS current_employees;

CREATE TABLE current_employees AS
SELECT ID, FirstName, Country, Role
FROM read_files(
  '/Volumes/dbacademy/' || DA.schema_name || '/myfiles/',
  format => 'csv',
  header => true,
  inferSchema => true
);

SELECT * FROM current_employees;
```

The `CREATE TABLE` statement creates a **Delta table** by default. No `USING DELTA` needed.

### Python equivalent

```python
# Read CSV into DataFrame
sdf = (spark
       .read
       .format("csv")
       .option("header", "true")
       .option("inferSchema", "true")
       .load(f"/Volumes/dbacademy/{DA.schema_name}/myfiles/"))

# Write as Delta managed table
(sdf
 .write
 .mode("overwrite")
 .format("delta")
 .saveAsTable(f"dbacademy.{DA.schema_name}.current_employees_py"))

# Read back
spark.read.table(f"dbacademy.{DA.schema_name}.current_employees_py").display()
```

### DESCRIBE commands

```sql
-- Detailed storage info: format, location, numFiles, sizeInBytes
DESCRIBE DETAIL current_employees;

-- Column metadata + table metadata (Type: Managed/External, provider, location)
DESCRIBE EXTENDED current_employees;

-- All Delta versions with timestamps and operations
DESCRIBE HISTORY current_employees;
```

**Managed vs External**: `DESCRIBE EXTENDED` → scroll to `Type` row. Managed tables have their data lifecycle controlled by Databricks (DROP TABLE removes data). External tables point to user-managed storage.

### DML operations

```sql
-- Insert
INSERT INTO current_employees VALUES
    (5555, 'Alex', 'USA', 'Instructor'),
    (6666, 'Sanjay', 'India', 'Instructor');

-- Update
UPDATE current_employees
  SET Role = 'Senior Manager'
  WHERE ID = 1111;

-- Delete
DELETE FROM current_employees
  WHERE ID = 3333;
```

Each operation creates a new version in the Delta transaction log.

### Time travel

```sql
-- By version number
SELECT * FROM current_employees VERSION AS OF 0;
SELECT * FROM current_employees VERSION AS OF 2;

-- Shorthand syntax
SELECT * FROM current_employees@v2;
```

> ⚠️ **DBR 18 breaking change:** `VERSION AS OF` or `TIMESTAMP AS OF` beyond `deletedFileRetentionDuration` now raises an error (was a warning). Aggressive `VACUUM` (< 7 days) blocks time travel.

## Open questions

- What is the default `deletedFileRetentionDuration` on Free Edition?

## Related sources

- [[ingesting-data]] — extends COPY INTO and incremental loading
- [[ch05-delta-lake-fundamentals]] — full explanatory chapter
