# Work with foreign tables

> **Source:** [docs.databricks.com/aws/en/tables/foreign](https://docs.databricks.com/aws/en/tables/foreign)
> **Added:** 2026-06-25
> **Source updated:** 2026-04-29
> **Tags:** tables, unity-catalog, foreign, federation, lakehouse-federation, query-federation, catalog-federation, hive-metastore, read-only, B4, A7
> **Type:** documentation

## Summary

The third Unity Catalog **table type** alongside [[managed-tables]] and [[external-tables]]. A **foreign table** (also called a **federated table**) belongs to a **foreign catalog** in Unity Catalog, but its data and metadata stay in an external system. Unity Catalog adds a governance layer on top, so you can query that external data through UC. It's the inbound half of Lakehouse Federation: you reach into someone else's system without moving the data. Almost always **read-only**, and it gives up UC's transactional guarantees and most performance optimizations — Databricks frames it as a migration/integration stopgap, not a destination.

## Key points

- **Two registration methods:** (1) **Query federation** — secure JDBC connections to external data *systems* (PostgreSQL, MySQL); (2) **Catalog federation** — connect external *catalogs* (Hive Metastore, AWS Glue, Snowflake Horizon Catalog) to query data directly in file storage.
- **Read-only by default.** External federated Hive metastore and *all* foreign tables accessed through Lakehouse Federation are read-only. The lone write exception: an **internal federated Hive metastore** (with sufficient privileges) lets you create/write foreign tables backed by it.
- **No UC transactional guarantees.** A foreign table may be backed by an ACID format (Delta, Iceberg), but UC doesn't manage its metadata/data/semantics, so you don't get managed-table transactional guarantees.
- **Most optimizations require UC.** Query-perf, enhanced write speed, data skipping, and metadata-only queries need a UC managed table — foreign tables miss them. Databricks recommends benchmarking foreign vs managed on the latest DBR.
- **Positioned as temporary.** Quick direct access without migration or ETL refactoring; migrate frequently-queried / production datasets to [[managed-tables]] (see [[convert-foreign-managed]]).
- **Hive-metastore back-compat:** foreign tables in a federated HMS return HMS metadata, including whether the table is a Hive *managed* or *external* table — for legacy Spark/Databricks workloads.

## Notes

### Why use a foreign table?

Flexibility when integrating with existing data systems or migrating off legacy ones. Many foreign tables are a **temporary** solution: direct access to data not managed by Databricks, with no data migration or upstream-ETL code refactoring required. Databricks recommends migrating datasets that drive production workloads or are queried frequently to **UC managed tables** for the performance and built-in optimizations (see [[convert-foreign-managed]]).

Query federation is also **complementary to Lakeflow Connect** — use it to load from external systems Lakeflow Connect doesn't support, and Databricks recommends **materialized views to replicate** a foreign table into UC (see query-federation `#load`).

### Create or write to foreign tables

- **Writable only via internal federated Hive metastore.** With sufficient privileges and a workspace configured with an internal federated HMS, you can create/write foreign tables backed by it.
- **Everything else is read-only:** external federated HMS + all Lakehouse-Federation-accessed foreign tables. (Minor gotcha: Catalog Explorer's **Updated by** reflects the last *metadata refresh* — the `session_user` who ran a query — not a data change.)
- **No transactional guarantees / fewer optimizations** (see Key points). Benchmark read+write latency and cost against a UC managed table.

> ⚠️ A foreign table can sit on top of Delta or Iceberg and still **not** behave like a UC table: UC doesn't own the metadata/data/semantics, so ACID + time-travel guarantees and most engine optimizations don't apply. Treat "backed by Delta" ≠ "managed Delta table."

## Quotes worth keeping

> "Foreign tables, sometimes referred to as federated tables, are tables registered using Unity Catalog as part of a foreign catalog. Foreign tables contain data and metadata managed by external systems, with Unity Catalog adding data governance to query these tables." (intro)

> "External federated Hive metastore and all foreign tables accessed through Lakehouse Federation are read-only." (Create or write to foreign tables)

## Open questions

- The page references a [[convert-foreign-managed]] migration path and a query-federation `#load` materialized-view pattern but doesn't detail them here — both now captured ([[convert-foreign-managed]], [[materialized-views]]).
- "Internal" vs "external" federated Hive metastore is the line between writable and read-only, but the page doesn't define internal-federated-HMS setup on this page.

## Related sources

- [[tables-concepts]] — parent overview placing foreign alongside managed/external/temporary as the UC table types.
- [[managed-tables]] — the recommended migration target; foreign is the read-only stopgap, managed is the governed/optimized destination.
- [[external-tables]] — the other non-managed type; external = *your* storage with UC metadata governance, foreign = *external system's* data+metadata with UC query governance.
- [[external-access]] — the outbound mirror (external engines reading UC data) vs foreign tables' inbound federation (UC reading external data).
