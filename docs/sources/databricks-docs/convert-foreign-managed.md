# Convert a foreign table to a managed Unity Catalog table

> **Source:** [docs.databricks.com/aws/en/tables/convert-foreign-managed](https://docs.databricks.com/aws/en/tables/convert-foreign-managed)
> **Added:** 2026-06-25
> **Source updated:** 2026-05-13
> **Tags:** tables, unity-catalog, foreign, managed, set-managed, federation, hms, glue, public-preview, B4
> **Type:** documentation

## Summary

The migration path *off* a [[foreign-tables|foreign table]] and into a UC **managed** table, via `ALTER TABLE … SET MANAGED {MOVE | COPY}` (Public Preview, **DBR 17.3+**). Only supports foreign tables federated through **HMS and Glue federation**. Conversion keeps the table's name, settings, permissions, views, and **history**, and opts the table into predictive optimization (`INHERIT`). `MOVE` cuts over in place (external/path access stops); `COPY` duplicates the data and leaves the source untouched.

## Video walkthrough

The docs page embeds a 10-minute YouTube walkthrough — federating an AWS Glue metastore and then converting foreign tables to managed. The **foreign-to-managed conversion begins at 5:30**.

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 1rem 0;">
  <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
    src="https://www.youtube.com/embed/0suBlnwHLUY?rel=0"
    title="Federate an AWS Glue metastore and convert foreign tables to managed"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen></iframe>
</div>

▶ Direct links: [full video](https://www.youtube.com/watch?v=0suBlnwHLUY) · [jump to foreign→managed at 5:30](https://www.youtube.com/watch?v=0suBlnwHLUY&t=330s)

## Key points

- **What it does:** `ALTER TABLE source_table SET MANAGED {MOVE | COPY}` turns a UC foreign table into a UC managed table.
- **Scope:** Public Preview; **only** foreign tables federated via **HMS / Glue federation**.
- **Preserved on conversion:** history, name, settings, permissions, views. Predictive optimization is set to `INHERIT` (schema/catalog default, currently off by default) — turn it on with `ALTER TABLE <t> ENABLE PREDICTIVE OPTIMIZATION`.
- **`MOVE`** — in-place cutover. External-catalog and **path-based access stop working**; all readers/writers must switch to UC **name-based** access (`catalog.schema.table`). Databricks readers/writers need **DBR 15.4 LTS+**; external clients need managed-table support ([Compatibility Mode](https://docs.databricks.com/aws/en/external-access/compatibility-mode)). Some downtime possible during conversion. Reversible with `UNSET MANAGED`.
- **`COPY`** — duplicates data into the managed storage location, leaving the source table in the external catalog intact (two copies). *You* are responsible for disabling reads/writes to the source and migrating workloads. Roll back by simply dropping the managed table (no `UNSET` needed).
- **Foreign-table drop semantics flip after conversion:** before conversion, dropping the source in the external catalog also drops the UC foreign table; after conversion to managed, dropping the source no longer affects the UC managed table.
- **Check it worked:** `DESCRIBE EXTENDED catalog.schema.table` → `Type` shows `MANAGED`.

## Notes

### Prerequisites

- **Data format** must be **Delta Lake** (for Parquet, do a one-time [Convert to Delta Lake](https://docs.databricks.com/aws/en/ingestion/data-migration/convert-to-delta) first).
- **HMS table type** must be an **external** HMS table — fails on a *managed* HMS table.
- **Runtime:** DBR **17.3+**.
- **Permissions:** `OWNER` or `MANAGE` on the table **and** `CREATE` on the `EXTERNAL LOCATION`.

### Rollback (MOVE)

Run `ALTER TABLE catalog.schema.my_managed_table UNSET MANAGED` to revert to an **external** table and regain source access; to get back to a *foreign* table, drop it and it re-federates as foreign on the next catalog sync.

> ⚠️ You **MUST** run `UNSET MANAGED` before dropping a `MOVE`-converted table — dropping without it can cause data loss/inconsistency. After rollback, commits made between conversion and rollback are time-travelable **by version but not by timestamp**, and managed-location data is deleted **7 days** after rollback.

### Known limitations

- **Streaming:** restart any streaming read/write jobs after conversion.
- **Cross-region cost:** if the metastore/catalog/schema default managed location is in a different cloud region from the foreign table's storage, you can incur cloud cross-region transfer charges (outside Databricks' control). Check with `DESCRIBE SCHEMA EXTENDED` / `DESCRIBE CATALOG EXTENDED` / `DESCRIBE METASTORE`.

### FAQ highlights

- **Create tables in a foreign catalog?** Yes. For **Glue/eHMS** schemas or schemas with a UC managed location, `CREATE TABLE foreign_catalog.schema.table` makes a UC managed/external table (not synced to the external catalog). For **internal HMS** connections it still creates a foreign table + an `hive_metastore` table; for **legacy workspace HMS** (read+write federation) it also creates the table in the internal HMS.
- **DBFS-backed foreign tables:** the current DBFS→cloud path mapping is stored as the external table's cloud path on conversion.
- **Bulk convert a whole schema/catalog:** iterate per-table, or use the **discoverx** labs project, e.g. `dx.from_tables("prod.*.*").with_sql("ALTER TABLE {full_table_name} SET MANAGED;").apply()`.

## Quotes worth keeping

> "This feature only supports converting foreign tables federated using HMS and Glue Federation." (Public Preview banner)

> "Converts the table to managed and disables access to the source table in the external catalog." (`MOVE`)

## Related sources

- [[foreign-tables]] — the table type this migrates away from; foreign is positioned as a stopgap, managed as the destination.
- [[convert-external-managed]] — the sibling `SET MANAGED` flow for *external* (not foreign) Delta tables; shares the MOVE/COPY mechanics, downtime notes, and legacy-reader caveats.
- [[managed-tables]] — the target type and the optimizations (predictive optimization, etc.) you gain.
