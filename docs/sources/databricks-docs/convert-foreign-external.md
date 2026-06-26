# Convert a foreign table to an external Unity Catalog table

> **Source:** [docs.databricks.com/aws/en/tables/convert-foreign-external](https://docs.databricks.com/aws/en/tables/convert-foreign-external)
> **Added:** 2026-06-25
> **Source updated:** 2026-05-13
> **Tags:** tables, unity-catalog, foreign, external, set-external, federation, hms, glue, public-preview, B4
> **Type:** documentation

`ALTER TABLE … SET EXTERNAL` converts a [[foreign-tables|foreign table]] into a UC **external** table: Unity Catalog takes over governance of the metadata, but the data files stay exactly where they are — nothing is moved or copied. It's the lighter sibling of [[convert-foreign-managed]] (`SET MANAGED MOVE`/`COPY`). Pick it over `SET MANAGED` when you want UC to govern the table but **don't** want managed-table behavior (auto-optimization, managed storage) or the data movement that `MOVE`/`COPY` involves.

```sql
ALTER TABLE source_table SET EXTERNAL [DRY RUN];
```

`DRY RUN` checks whether the table can be upgraded without doing it (returns `DRY_RUN_SUCCESS`). Conversion **preserves** history, name, settings, permissions, and views, and supports a broad set of formats — **Delta, Parquet, ORC, Avro, JSON, CSV, TEXT** (foreign→managed is Delta-only). It's **Public Preview**, needs **DBR 17.3+**, and only works on foreign tables federated through **HMS or Glue federation**.

Two behavior changes worth noting: **rollback is just a drop** — `DROP TABLE catalog.schema.my_external_table`, and the table re-federates as foreign on the next catalog sync (no `UNSET` step, unlike foreign→managed). And **drop semantics flip**: before conversion, dropping the source in the external catalog also drops the UC foreign table; after, dropping the source no longer affects the UC external table.

## Prerequisites

- **Data format:** one of Delta, Parquet, ORC, Avro, JSON, CSV, TEXT.
- **HMS table type:** must be an **external** HMS table — fails on a *managed* HMS table.
- **Runtime:** DBR **17.3+**.
- **Permissions:** `OWNER` or `MANAGE` on the table, plus `CREATE` on the `EXTERNAL LOCATION`.

> ⚠️ Concurrent writes — to the source table and from Unity Catalog — are not supported. Disable reads/writes to the source in the external catalog and migrate workloads to the new catalog **before** converting.

## Verify the conversion

Check in **Catalog Explorer**: the table shows as **Foreign** before and **External** after.

> 📌 Don't trust `DESCRIBE EXTENDED` — it reports the type as `EXTERNAL` **both before and after** conversion (federation mimics running the command against `hive_metastore`), so it's not a reliable signal. Use Catalog Explorer.

## FAQ

- **Create tables in a foreign catalog?** Same as foreign→managed: for **Glue/eHMS** schemas or schemas with a UC managed location, `CREATE TABLE foreign_catalog.schema.table` makes a UC managed/external table (not synced out); **internal HMS** connections also create an `hive_metastore` table; **legacy workspace HMS** (read+write federation) also creates it in the internal HMS.
- **Parquet SerDe tables in Glue:** fix the Glue table metadata first — set `spark.sql.sources.provider = PARQUET` and `spark.sql.partitionProvider = filesystem` (and the SerDe `path`) via the AWS `boto3` `update_table` API before converting. The docs page ships a ready-made script.
- **DBFS-backed tables:** the current DBFS→cloud path mapping is stored as the external table's cloud path on conversion.
- **Bulk convert a schema/catalog:** iterate per-table, or use the **discoverx** labs project — `dx.from_tables("prod.*.*").with_sql("ALTER TABLE {full_table_name} SET EXTERNAL;").apply()` (use `.explain()` for a dry run).

Related: [[convert-foreign-managed]], [[foreign-tables]], [[external-tables]], [[convert-external-managed]].
