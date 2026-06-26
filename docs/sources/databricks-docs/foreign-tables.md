# Work with foreign tables

> **Source:** [docs.databricks.com/aws/en/tables/foreign](https://docs.databricks.com/aws/en/tables/foreign)
> **Added:** 2026-06-25
> **Source updated:** 2026-04-29
> **Tags:** tables, unity-catalog, foreign, federation, lakehouse-federation, query-federation, catalog-federation, hive-metastore, read-only, B4, A7
> **Type:** documentation

A **foreign table** (also called a **federated table**) is the third Unity Catalog table type, alongside [[managed-tables]] and [[external-tables]]. It belongs to a **foreign catalog** in Unity Catalog, but its data *and* metadata stay in an external system — UC only adds a governance layer so you can query that external data through it. This is the inbound half of Lakehouse Federation: you reach into another system without moving the data. Foreign tables are almost always **read-only**, give up UC's transactional guarantees and most performance optimizations, and Databricks frames them as a migration/integration stopgap rather than a destination.

There are two ways to register one:

- **Query federation** — secure JDBC connections to external data *systems* (PostgreSQL, MySQL).
- **Catalog federation** — connect external *catalogs* (Hive Metastore, AWS Glue, Snowflake Horizon Catalog) to query data directly in file storage.

> "Foreign tables, sometimes referred to as federated tables, are tables registered using Unity Catalog as part of a foreign catalog. Foreign tables contain data and metadata managed by external systems, with Unity Catalog adding data governance to query these tables."

## Why use a foreign table?

Flexibility when integrating with existing data systems or migrating off legacy ones. Many foreign tables are a **temporary** solution: direct access to data Databricks doesn't manage, with no data migration or upstream-ETL refactoring required. Databricks recommends migrating datasets that drive production workloads or are queried frequently to **UC managed tables** for the performance and built-in optimizations (see [[convert-foreign-managed]]).

Query federation is also **complementary to Lakeflow Connect** — use it to load from external systems Lakeflow Connect doesn't support, and Databricks recommends **materialized views to replicate** a foreign table into UC (see [[materialized-views]]).

## Create or write to foreign tables

Foreign tables are **writable only via an internal federated Hive metastore**: with sufficient privileges and a workspace configured with one, you can create and write foreign tables backed by it. **Everything else is read-only** — an external federated HMS and all foreign tables accessed through Lakehouse Federation.

> "External federated Hive metastore and all foreign tables accessed through Lakehouse Federation are read-only."

A few things to keep in mind:

- **No UC transactional guarantees.** A foreign table can sit on Delta or Iceberg and still **not** behave like a UC table — UC doesn't own the metadata/data/semantics, so ACID + time-travel guarantees don't apply. "Backed by Delta" ≠ "managed Delta table."
- **Most optimizations require a managed table.** Query performance, enhanced write speed, data skipping, and metadata-only queries need a UC managed table; foreign tables miss them. Benchmark read/write latency and cost against a managed table on the latest DBR.
- **Hive-metastore back-compat:** foreign tables in a federated HMS return HMS metadata, including whether the table is Hive *managed* or *external* — for legacy Spark/Databricks workloads.
- **Catalog Explorer gotcha:** **Updated by** reflects the last *metadata refresh* (the `session_user` who ran a query), not a data change.

Related: [[tables-concepts]], [[managed-tables]], [[external-tables]], [[external-access]], [[convert-foreign-managed]], [[materialized-views]].
