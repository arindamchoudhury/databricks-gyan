# Convert a foreign table to an external Unity Catalog table

> **Source:** [docs.databricks.com/aws/en/tables/convert-foreign-external](https://docs.databricks.com/aws/en/tables/convert-foreign-external)
> **Added:** 2026-06-25
> **Source updated:** 2026-05-13
> **Tags:** tables, unity-catalog, foreign, external, set-external, federation, hms, glue, public-preview, B4
> **Type:** documentation

## Summary

The lighter sibling of [[convert-foreign-managed]]. `ALTER TABLE … SET EXTERNAL` converts a [[foreign-tables|foreign table]] into a UC **external** table — UC takes over governance of the metadata, but the data files stay where they are. No data is moved or copied. It's Public Preview, needs **DBR 17.3+**, and only works on foreign tables federated through **HMS or Glue federation**.

Pick this over `SET MANAGED` when you want UC to govern the table but don't want managed-table behavior (auto-optimization, managed storage) or the data movement that `MOVE`/`COPY` involves.

## Key points

- **What it does:** `ALTER TABLE source_table SET EXTERNAL [DRY RUN]` turns a UC foreign table into a UC external table. Data files are untouched.
- **Scope:** Public Preview. Only foreign tables federated via **HMS / Glue federation**.
- **Preserved on conversion:** history, name, settings, permissions, views.
- **Broader format support than `SET MANAGED`:** Delta, Parquet, ORC, Avro, JSON, CSV, TEXT. (Foreign→managed is Delta-only.)
- **`DRY RUN`** checks whether the table can be upgraded without actually doing it. Returns `DRY_RUN_SUCCESS` if it can.
- **Rollback is just a drop.** `DROP TABLE catalog.schema.my_external_table` — the table re-federates as foreign on the next catalog sync. No `UNSET` step (unlike foreign→managed `MOVE`).
- **Drop semantics flip after conversion.** Before: dropping the source in the external catalog also drops the UC foreign table. After: dropping the source no longer affects the UC external table.

## Notes

### Prerequisites

- **Data format:** one of Delta, Parquet, ORC, Avro, JSON, CSV, TEXT.
- **HMS table type:** must be an **external** HMS table. Fails on a *managed* HMS table.
- **Runtime:** DBR **17.3+**.
- **Permissions:** `OWNER` or `MANAGE` on the table, plus `CREATE` on the `EXTERNAL LOCATION`.

> ⚠️ Concurrent writes — to the source table and from Unity Catalog — are not supported. Disable reads/writes to the source in the external catalog and migrate workloads to the new catalog **before** converting.

### Verifying the conversion (don't trust `DESCRIBE EXTENDED`)

Check in **Catalog Explorer**: the table shows as **Foreign** before and **External** after.

> 📌 `DESCRIBE EXTENDED` reports the type as `EXTERNAL` **both before and after** conversion — federation mimics the behavior of running the command against `hive_metastore`, so it's not a reliable signal. Use Catalog Explorer instead.

### FAQ highlights

- **Create tables in a foreign catalog?** Same behavior as foreign→managed: for **Glue/eHMS** schemas or schemas with a UC managed location, `CREATE TABLE foreign_catalog.schema.table` makes a UC managed/external table (not synced out); **internal HMS** connections also create an `hive_metastore` table; **legacy workspace HMS** (read+write federation) also creates the table in the internal HMS.
- **Parquet SerDe tables in Glue:** you must fix the Glue table metadata first — set `spark.sql.sources.provider = PARQUET` and `spark.sql.partitionProvider = filesystem` (and the SerDe `path`) via the AWS `boto3` `update_table` API before converting. The docs page ships a ready-made script.
- **DBFS-backed tables:** the current DBFS→cloud path mapping is stored as the external table's cloud path on conversion.
- **Bulk convert a schema/catalog:** iterate per-table, or use the **discoverx** labs project — `dx.from_tables("prod.*.*").with_sql("ALTER TABLE {full_table_name} SET EXTERNAL;").apply()` (use `.explain()` for a dry run).

## Quotes worth keeping

> "Use the `SET EXTERNAL` feature to convert a foreign table to a Unity Catalog `EXTERNAL` table." (overview)

> "Running `DESCRIBE EXTENDED` shows the table type as `EXTERNAL` both before and after conversion. … To accurately verify conversion, use Catalog Explorer." (Check conversion)

## Related sources

- [[convert-foreign-managed]] — the heavier sibling (`SET MANAGED MOVE`/`COPY`): moves/copies data into managed storage, Delta-only, gains predictive optimization, `UNSET MANAGED` rollback. Use external when you want governance without managed-table behavior or data movement.
- [[foreign-tables]] — the source type both conversions migrate away from.
- [[external-tables]] — the target type: UC governs metadata, data files stay at a `LOCATION` you keep, `DROP` leaves the data.
- [[convert-external-managed]] — the next hop if you later want managed: external→managed via `SET MANAGED`.
