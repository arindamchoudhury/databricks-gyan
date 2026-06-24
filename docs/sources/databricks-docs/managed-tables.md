# Unity Catalog managed tables

> **Source:** [docs.databricks.com/aws/en/tables/managed](https://docs.databricks.com/aws/en/tables/managed)
> **Added:** 2026-06-23
> **Source updated:** 2026-06-17
> **Tags:** tables, unity-catalog, managed, delta, iceberg, predictive-optimization, catalog-commits, undrop, recovery-period, B4
> **Type:** documentation

## Summary

Deep-dive on the **default + recommended** table type from [[tables-concepts]]. Unity Catalog managed tables hand UC full control of read/write/storage/optimization. Data files live in the **schema- or catalog-level managed storage location**. The page's core is a feature table of capabilities **unique to managed tables** (not on external/foreign), plus the create/drop SQL and the configurable UNDROP recovery period.

> This page is **Unity Catalog only**. For managed tables in the legacy Hive metastore, see "Database objects in the legacy Hive metastore" — a separate model.

## Key points

- UC manages **all** read, write, storage, and optimization responsibilities.
- Data files stored in the **containing schema or catalog's managed storage location** (not a path you pick per-table).
- **Path-based access is not supported** (except Compatibility Mode) — it bypasses UC access controls and risks corruption/loss. Always use `catalog.schema.table` names.
- Six recommended benefits vs external/foreign: lower storage+compute cost, faster queries across all clients, automatic maintenance/optimization, secure external-client access via open APIs, Delta **and** Iceberg support, automatic upgrades to latest platform features.
- Default format = Delta. **Iceberg requires explicit `USING iceberg`** or you get Delta.

## Notes

### Features unique to managed tables

Not available on external/foreign tables. Watch the default-on vs default-off column — most are **off by default**.

| Feature | What it does | Default / config |
|---|---|---|
| **Catalog commits** | Multi-statement txns across tables, faster planning (metadata served from UC directly), enforceable schema/constraint changes, safe writes from external engines | **Off.** Set `delta.feature.catalogManaged` table property |
| **Predictive optimization** | AI auto-runs `OPTIMIZE` (compact + incremental clustering), `VACUUM` (delete unused files), `ANALYZE` (stats for data skipping) — no manual maintenance | **On for new accounts ≥ Nov 11 2024**; rolling out to existing accounts. Databricks recommends enabling for **all** managed tables |
| **Multi-statement transactions** | Many SQL statements across ≥1 table as one atomic commit, full ACID, all-or-nothing | **Off.** Delta = Public Preview, Iceberg = Private Preview. `BEGIN ATOMIC...END;` (non-interactive) or `BEGIN TRANSACTION;...COMMIT;` (interactive) |
| **Automatic liquid clustering** | For PO-enabled tables: auto-picks clustering keys and updates them as query patterns shift | **Off** |
| **Metadata caching** | In-memory cache of txn metadata → fewer requests to the cloud-stored transaction log | **On. Not configurable** |
| **Full-text search indexes** | Speeds substring/keyword lookups via `search`/`isearch` functions; skips files that can't match | **Off.** Beta, needs **DBR 18.2+**. `CREATE SEARCH INDEX` |
| **Auto file deletion on DROP** | After DROP + recovery period (default 7 days), UC deletes data files in cloud storage. External tables = you delete files manually | **On.** Recovery period configurable at catalog/schema level |

> The Delta-vs-Iceberg split shows up here: catalog commits + multi-statement txns are GA/preview on Delta first; Iceberg lags (Iceberg txns = Private Preview). Confirms [[tables-concepts]]'s point that Delta is the more featureful default.

### Access from external systems

Managed tables are **interoperable**, not locked in — readable/writable by Delta Lake and Apache Iceberg clients.

- External engines: Trino, DuckDB, Apache Spark, Daft, and IRC-integrated engines (e.g. Dremio).
- **Compatibility Mode** — for clients that don't support open APIs; read managed tables with any Delta/Iceberg client (and the only sanctioned path-based access).
- **OpenSharing** (open-source protocol, formerly Delta Sharing) — secure governed sharing with external partners; grant temporary, **read-only** access.

Two open APIs:

| API | Access |
|---|---|
| **Unity REST API** | Read/write/create for Delta Lake clients → managed Delta tables |
| **Iceberg REST Catalog (IRC)** | Read/write/create for Iceberg clients → managed Iceberg tables; **read-only** on Delta tables that have Iceberg reads enabled (UniForm) |

Both support **credential vending**: temporary scoped creds that inherit the requesting principal's privileges, preserving governance.

### Create a managed table

Privileges: `USE CATALOG` (parent catalog) + `USE SCHEMA` (parent schema) + `CREATE TABLE` (parent schema).

```sql
-- Create a managed Delta table
CREATE TABLE <catalog-name>.<schema-name>.<table-name>
(
  <column-specification>
);

-- Create a managed Iceberg table
CREATE TABLE <catalog-name>.<schema-name>.<table-name>
(
  <column-specification>
)
USING iceberg;
```

- **`USING iceberg` is required** for Iceberg — default is Delta.
- For managed Iceberg, Databricks periodically runs **serverless** metadata-optimization jobs; that compute gets `MODIFY` scoped to the table only for the job duration and only writes metadata.
- **Clone**: managed Delta supports deep + shallow clone; managed Iceberg supports **deep only**.

You can also create managed tables from query results or DataFrame write operations. Patterns the docs cross-link (each is its own article):

- **[`CREATE TABLE [USING]`](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-table-using)** — explicit DDL with column spec / `USING` format (above).
- **[`CREATE TABLE LIKE`](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-table-like)** — copy another table's schema (and clustering config) without data.
- **[Create or modify a table using file upload](https://docs.databricks.com/aws/en/ingestion/create-or-modify-table)** — UI-driven create from an uploaded CSV/TSV/JSON/Avro/Parquet file.
- **CTAS / DataFrame writes** — `CREATE TABLE … AS SELECT`, or `df.write.saveAsTable(...)` / `.writeTo(...)`.

### Drop a managed table

Privileges: `MANAGE` on the table (or be owner) + `USE SCHEMA` + `USE CATALOG`.

```sql
DROP TABLE IF EXISTS catalog_name.schema_name.table_name;
```

- **`UNDROP TABLE`** recovers accidental drops. Default recoverable window = **7 days**.
- After the recovery period ends, Databricks deletes underlying data files from cloud tenant **within 48 hours**.

### Configure the recovery period (Public Preview)

Set per catalog or schema; **schema-level wins** over catalog-level for tables in that schema. Needs `MANAGE` or ownership. Applies **only to tables dropped after** it's set — not retroactive.

- Allowed: **0 hours** (disables UNDROP recovery) or **7–30 days** inclusive.
- Longer (up to 30 d) = more protection for critical prod data. Shorter / 0 = faster deletion → cost savings for ETL that frequently creates/drops tables. With 0, dropped tables are unrecoverable and files deleted within 48 h.

```sql
-- Set a 30-day recovery period on a catalog
ALTER CATALOG my_catalog RETAIN DROPPED TO 30 DAYS;

-- Set a 7-day recovery period on a schema (overrides the catalog setting)
ALTER SCHEMA my_catalog.my_schema RETAIN DROPPED TO 7 DAYS;

-- Or at creation time
CREATE CATALOG my_catalog RETAIN DROPPED FOR 30 DAYS;
CREATE SCHEMA my_catalog.my_schema RETAIN DROPPED FOR 7 DAYS;

-- Check it (look for the "Recovery Period Hours" row)
DESCRIBE CATALOG EXTENDED my_catalog;
DESCRIBE SCHEMA EXTENDED my_catalog.my_schema;
```

## Quotes worth keeping

> "Path-based access to Unity Catalog managed tables is not supported (except in Compatibility Mode) because it bypasses Unity Catalog access controls, and might result in possible data corruption or loss." (Access Databricks data using external systems)

## Open questions

- ~~Catalog commits (`delta.feature.catalogManaged`) overlaps conceptually with multi-statement transactions — both enable cross-table atomic writes. Relationship between the two features isn't spelled out on this page.~~ **Answered** by [[catalog-commits]]: catalog commits is the *coordination substrate* (commits move from per-table log → Unity Catalog); multi-statement transactions are the *capability* it unlocks.

## Related sources

- [[tables-concepts]] — parent page; defines the three table types. This page is the managed-table deep-dive it links to.
- [[catalog-commits]] — deep-dive on the catalog commits feature listed in this page's feature table; answers the open question above.
- [[ch03-mastering-relational-entities]] — DCDE-SG book chapter (DBR 13.3-era) that frames tables as managed-vs-external on `hive_metastore`; this page is pure UC and corrects that.
- [[ch02-managing-data-with-delta-lake]] — OPTIMIZE / VACUUM / liquid clustering / predictive optimization mechanics referenced in the feature table.

## References

- [Unity Catalog managed tables](https://docs.databricks.com/aws/en/tables/managed) — this page
- Learning path: **B4 — Spark SQL & Relational Entities**
