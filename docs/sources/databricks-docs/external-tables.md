# Unity Catalog external tables

> **Source:** [docs.databricks.com/aws/en/tables/external](https://docs.databricks.com/aws/en/tables/external)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-17
> **Tags:** tables, unity-catalog, external, delta, external-location, storage-credential, drop-table, repair-table, B4
> **Type:** documentation

## Summary

The non-default counterpart to [[managed-tables]]. A Unity Catalog **external table** keeps its data files in cloud object storage **in your tenant, at a location you pick**. UC governs the **metadata** (full governance on queries) but **not** the data lifecycle, optimization, storage location, or layout. You must point the table at a registered **external location**; dropping the table removes metadata only — **data files stay**. Databricks recommends managed tables in most cases; external tables exist for non-UC-compatible formats (JSON/Avro) and direct non-Databricks client access.

> Unity Catalog only. External tables in the **legacy Hive metastore** behave differently — see "Database objects in the legacy Hive metastore".

## Key points

- Data files live in **your cloud storage**; UC manages metadata, not lifecycle/optimization/location/layout.
- A **storage location is mandatory** at create time — must be a UC-registered **external location**.
- **DROP removes metadata only.** Underlying data files are **not** deleted — delete them manually if needed.
- File formats: **DELTA, CSV, JSON, AVRO, PARQUET, ORC, TEXT** (broader than managed, which is Delta/Iceberg).
- Two recommended use cases only: (1) register existing data in a format UC managed tables don't support (JSON, Avro); (2) direct access from non-Databricks clients that don't support other external-access patterns. **UC privileges are NOT enforced** when external systems read the data files directly.
- Out-of-band metadata edits (non-Databricks client or path-based access) **don't sync** to UC → must run `MSCK REPAIR TABLE <name> SYNC METADATA`.

## Notes

### When to use external tables

Databricks recommends external tables only for:

- **Incompatible formats** — registering a table backed by existing data not compatible with UC managed tables, such as JSON or Avro.
- **Direct external-client access** — non-Databricks clients that don't support other external-access patterns. Caveat: **Unity Catalog privileges are not enforced when users access data files from external systems** (contrast with [[external-access]]'s credential-vending/Iceberg-REST patterns, which *do* keep UC governance in the loop).

Otherwise, use managed tables for automatic optimization, faster queries, lower cost. To move an external Delta table over, see [[convert-external-managed]].

> ⚠️ **IMPORTANT (out-of-band metadata).** If you update external table metadata via a non-Databricks client or path-based access from within Databricks, that metadata **does not auto-sync** with UC. Databricks recommends against it, but if you do, run `MSCK REPAIR TABLE <table-name> SYNC METADATA` to bring the UC schema up to date. See REPAIR TABLE.

### File formats

`DELTA` · `CSV` · `JSON` · `AVRO` · `PARQUET` · `ORC` · `TEXT`

> 💡 **Clarification (not on page) — `DELTA` is a *table* format, not a flat file format.** The list is really the set of `USING <format>` values for `CREATE TABLE … LOCATION …`. `CSV/JSON/AVRO/PARQUET/ORC/TEXT` are raw file formats — an external table over them is a UC metadata pointer over dumb files: no transaction log, no ACID/time-travel. `DELTA` sits a layer above (Parquet data files **+** a `_delta_log/` JSON transaction log), so an external **Delta** table gets full ACID/time-travel. That's why Databricks recommends external tables mainly for the **non-Delta** formats UC managed tables can't hold (JSON, Avro); for Delta you'd usually prefer a **managed** table.

### Create an external table

**Before you begin** — you must first configure an **external location** granting access to your cloud storage. Databricks recommends the **AWS CloudFormation Quickstart** template, which configures both the storage credential and external location in one step.

**Permissions required:**

- `CREATE EXTERNAL TABLE` on the external location granting access to the `LOCATION`.
- `USE CATALOG` on the parent catalog.
- `USE SCHEMA` on the parent schema.
- `CREATE TABLE` on the parent schema.

> **NOTE (multi-metastore S3).** When an S3 external location is associated with multiple metastores, **avoid granting write access** — writes from different metastores to the same external table can cause consistency issues. **Reading** the same S3 location across metastores is safe.

**SQL** — placeholders: `<catalog>`, `<schema>`, `<table-name>`, `<column-specification>`, `<bucket-path>`, `<table-directory>` (use a **unique directory per table**). Table paths must be **standard ASCII only** (A–Z, a–z, 0–9, and common symbols like `/ _ -`).

```sql
CREATE TABLE <catalog>.<schema>.<table-name>
(
  <column-specification>
)
LOCATION 's3://<bucket-path>/<table-directory>';
```

See CREATE TABLE for full parameters.

> 💡 **Clarification (not on page) — "the table will be created" = create *new* empty table, not register existing.** The example above (with `<column-specification>`) defines a **brand-new, empty** external table: you declare the schema, and `LOCATION` is where its data files **will** live in your cloud storage. Data is **not** there yet — it lands when you `INSERT`/write (hence "use a **unique** directory per table" — fresh, non-colliding). Creating the table makes the **table object + storage directory** (for Delta, a `_delta_log/` is written there); `DROP TABLE` later removes metadata, leaves whatever you wrote.
>
> The other pattern — **registering existing data** — points `LOCATION` at a path that **already has** data files, with **no column spec** (schema inferred):
>
> ```sql
> CREATE TABLE <catalog>.<schema>.<table-name>
> USING DELTA
> LOCATION 's3://<bucket-path>/<existing-data-dir>';   -- no columns; read from files
> ```
>
> | | Create new (example above) | Register existing |
> |---|---|---|
> | Column spec | yes, you define it | no, inferred from files |
> | Data at `LOCATION` | empty → written later | already present |
> | What "create" does | table object + storage dir | metadata pointer over existing files |

**DataFrame write operations** — you can also create external tables from query results or DataFrame writes. Use the `LOCATION` clause to set the external path. These SQL forms work with DataFrame ops:

- `CREATE TABLE [USING]`
- `CREATE TABLE LIKE`

### Drop an external table

Must be the table **owner** or hold `MANAGE` on the table.

```sql
DROP TABLE IF EXISTS catalog_name.schema_name.table_name;
```

UC **does not delete** the underlying cloud-storage data on drop. Delete the data files directly if you need the data gone. (Mirror image of managed tables, where drop schedules data for deletion within the UNDROP recovery period — see [[managed-tables]].)

### Example notebook

Databricks ships a "Create and manage an external table in Unity Catalog" notebook that creates a catalog, schema, and external table and manages permissions. Recommends running the CloudFormation Quickstart first to set up the external location.

## Quotes worth keeping

> "When you drop an external table, Unity Catalog removes the table metadata but does not delete the underlying data files." (When to use external tables)

> "Unity Catalog privileges are not enforced when users access data files from external systems." (When to use external tables)

## Open questions

- The page lists DELTA among external formats but doesn't mention Iceberg — external tables presumably can't be Iceberg-managed the way managed tables can. Unconfirmed here.

## Related sources

- [[managed-tables]] — the default/recommended counterpart; external is the opt-out for incompatible formats or direct external access.
- [[tables-concepts]] — parent overview placing external alongside managed/foreign/temporary table types.
- [[convert-external-managed]] — migration path off external Delta tables into managed.
- [[external-access]] — the *other* way to reach UC data from outside (credential vending, Iceberg REST) that **keeps** UC governance, unlike raw external-table file access.
- [[managed-storage]] — where managed-table data lives; external tables instead use a per-table `LOCATION` you choose.
