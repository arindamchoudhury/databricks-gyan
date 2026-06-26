# Unity Catalog managed tables

> **Source:** [docs.databricks.com/aws/en/tables/managed](https://docs.databricks.com/aws/en/tables/managed)
> **Added:** 2026-06-23
> **Source updated:** 2026-06-17
> **Tags:** tables, unity-catalog, managed, delta, iceberg, predictive-optimization, catalog-commits, undrop, recovery-period, B4
> **Type:** documentation

Managed tables are the **default and recommended** table type from [[tables-concepts]]: Unity Catalog takes full control of read, write, storage, and optimization. Data files live in the **schema- or catalog-level managed storage location** (not a path you pick per-table), and **path-based access is not supported** (except Compatibility Mode) because it bypasses UC access controls and risks corruption/loss — always use `catalog.schema.table` names. Default format is **Delta**; **Iceberg requires explicit `USING iceberg`** or you get Delta.

> "Path-based access to Unity Catalog managed tables is not supported (except in Compatibility Mode) because it bypasses Unity Catalog access controls, and might result in possible data corruption or loss."

Databricks lists six benefits over external/foreign tables: lower storage + compute cost, faster queries across all clients, automatic maintenance/optimization, secure external-client access via open APIs, Delta **and** Iceberg support, and automatic upgrades to the latest platform features. This page is **Unity Catalog only** — managed tables in the legacy Hive metastore are a separate model.

## Features unique to managed tables

Not available on external/foreign tables. Watch the default-on vs default-off column — most are **off by default**.

| Feature | What it does | Default / config |
|---|---|---|
| **Catalog commits** | Multi-statement txns across tables, faster planning (metadata served from UC directly), enforceable schema/constraint changes, safe writes from external engines | **Off.** Set `delta.feature.catalogManaged` table property |
| **Predictive optimization** | AI auto-runs `OPTIMIZE` (compact + incremental clustering), `VACUUM` (delete unused files), `ANALYZE` (stats for data skipping) | **On for new accounts ≥ Nov 11 2024**; rolling out to existing. Recommended for **all** managed tables |
| **Multi-statement transactions** | Many SQL statements across ≥1 table as one atomic, all-or-nothing commit | **Off.** Delta = Public Preview, Iceberg = Private Preview. `BEGIN ATOMIC…END;` or `BEGIN TRANSACTION;…COMMIT;` |
| **Automatic liquid clustering** | For PO-enabled tables: auto-picks clustering keys and updates them as query patterns shift | **Off** |
| **Metadata caching** | In-memory cache of txn metadata → fewer requests to the cloud-stored transaction log | **On. Not configurable** |
| **Full-text search indexes** | Speeds substring/keyword lookups via `search`/`isearch`; skips files that can't match | **Off.** Beta, needs **DBR 18.2+**. `CREATE SEARCH INDEX` |
| **Auto file deletion on DROP** | After DROP + recovery period (default 7 days), UC deletes data files in cloud storage | **On.** Recovery period configurable at catalog/schema level |

> The Delta-vs-Iceberg split shows here: catalog commits + multi-statement txns are GA/preview on Delta first; Iceberg lags (Iceberg txns = Private Preview). Confirms [[tables-concepts]]'s point that Delta is the more featureful default.

## Access from external systems

Managed tables are **interoperable**, not locked in — readable/writable by Delta Lake and Apache Iceberg clients (Trino, DuckDB, Apache Spark, Daft, IRC-integrated engines like Dremio).

- **Compatibility Mode** — for clients that don't support open APIs; read managed tables with any Delta/Iceberg client (and the only sanctioned path-based access).
- **OpenSharing** (open-source protocol, formerly Delta Sharing) — secure governed sharing with external partners; grant temporary, **read-only** access.

Two open APIs, both supporting **credential vending** (temporary scoped creds that inherit the requesting principal's privileges, preserving governance):

| API | Access |
|---|---|
| **Unity REST API** | Read/write/create for Delta Lake clients → managed Delta tables |
| **Iceberg REST Catalog (IRC)** | Read/write/create for Iceberg clients → managed Iceberg tables; **read-only** on Delta tables with Iceberg reads enabled (UniForm) |

## Create a managed table

Privileges: `USE CATALOG` (parent catalog) + `USE SCHEMA` (parent schema) + `CREATE TABLE` (parent schema).

```sql
-- Managed Delta table (default)
CREATE TABLE <catalog-name>.<schema-name>.<table-name>
(
  <column-specification>
);

-- Managed Iceberg table
CREATE TABLE <catalog-name>.<schema-name>.<table-name>
(
  <column-specification>
)
USING iceberg;
```

- **`USING iceberg` is required** for Iceberg — default is Delta.
- For managed Iceberg, Databricks periodically runs **serverless** metadata-optimization jobs; that compute gets `MODIFY` scoped to the table only for the job duration, and only writes metadata.
- **Clone:** managed Delta supports deep + shallow clone; managed Iceberg supports **deep only**.

You can also create managed tables from query results or DataFrame writes. The docs cross-link each pattern: `CREATE TABLE [USING]` (explicit DDL), `CREATE TABLE LIKE` (copy schema + clustering config, no data), "Create or modify a table using file upload" (UI from CSV/TSV/JSON/Avro/Parquet), and CTAS / DataFrame writes (`CREATE TABLE … AS SELECT`, `df.write.saveAsTable(...)` / `.writeTo(...)`).

## Drop a managed table

Privileges: `MANAGE` on the table (or be owner) + `USE SCHEMA` + `USE CATALOG`.

```sql
DROP TABLE IF EXISTS catalog_name.schema_name.table_name;
```

- **`UNDROP TABLE`** recovers accidental drops. Default recoverable window = **7 days**.
- After the recovery period ends, Databricks deletes the underlying data files from the cloud tenant **within 48 hours**.

## Configure the recovery period (Public Preview)

Set per catalog or schema; **schema-level wins** over catalog-level. Needs `MANAGE` or ownership, and applies **only to tables dropped after** it's set (not retroactive). Allowed values: **0 hours** (disables UNDROP) or **7–30 days** inclusive — longer for critical prod data, shorter/0 for ETL that frequently creates/drops tables (with 0, dropped tables are unrecoverable and files deleted within 48 h).

```sql
ALTER CATALOG my_catalog RETAIN DROPPED TO 30 DAYS;
ALTER SCHEMA my_catalog.my_schema RETAIN DROPPED TO 7 DAYS;   -- overrides the catalog
CREATE CATALOG my_catalog RETAIN DROPPED FOR 30 DAYS;          -- or at creation time
CREATE SCHEMA my_catalog.my_schema RETAIN DROPPED FOR 7 DAYS;
DESCRIBE CATALOG EXTENDED my_catalog;                          -- look for "Recovery Period Hours"
DESCRIBE SCHEMA EXTENDED my_catalog.my_schema;
```

Related: [[tables-concepts]], [[catalog-commits]], [[transactions]], [[predictive-optimization]], [[ch03-mastering-relational-entities]], [[ch02-managing-data-with-delta-lake]].
