# Predictive optimization for Unity Catalog managed tables

> **Source:** [docs.databricks.com/aws/en/optimizations/predictive-optimization](https://docs.databricks.com/aws/en/optimizations/predictive-optimization)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-18
> **Tags:** tables, unity-catalog, managed, delta, iceberg, predictive-optimization, optimize, vacuum, analyze, liquid-clustering, serverless, system-tables, B4, B5
> **Type:** documentation

Predictive optimization (PO) automatically runs `OPTIMIZE`, `VACUUM`, and `ANALYZE` on Unity Catalog **managed** tables (Delta and Iceberg), removing manual maintenance. Databricks identifies tables that would benefit, queues the operations, and collects statistics on write. "Predictive optimization is enabled by default for accounts created on or after November 11, 2024… This rollout is expected to complete by August 2026." It runs on **serverless jobs compute** (billed to a serverless jobs SKU), and Databricks recommends it for **all** managed tables.

## What operations it runs

| Operation | What PO does |
|---|---|
| `OPTIMIZE` | Triggers incremental clustering for enabled tables; improves perf by optimizing file sizes. |
| `VACUUM` | Reduces storage cost by deleting data files no longer referenced. |
| `ANALYZE` | Incremental update of statistics to improve query performance. |

> "OPTIMIZE does not run ZORDER when executed by predictive optimization. On tables that use Z-order, predictive optimization ignores Z-ordered files." (If automatic liquid clustering is enabled, PO might select new clustering keys before clustering data.)

## VACUUM retention warning

The retention window is `delta.deletedFileRetentionDuration` (default **7 days**); `VACUUM` removes unreferenced files within it. To keep data longer (e.g. extended time travel), set this **before** enabling PO:

```sql
ALTER TABLE table_name SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = '30 days');
```

## Prerequisites

Workspace on **Premium plan or above** in a supported region; **SQL warehouses** or **DBR 12.2 LTS+**; only **UC managed tables**.

## Enable / disable (inheritance model)

All UC managed tables inherit the **account** value by default; override at catalog or schema. Privileges: account admin (account), catalog owner (catalog), schema owner (schema). Account level: accounts console → Settings → Feature enablement.

```sql
ALTER CATALOG [catalog_name] { ENABLE | DISABLE | INHERIT } PREDICTIVE OPTIMIZATION;
ALTER { SCHEMA | DATABASE } schema_name { ENABLE | DISABLE | INHERIT } PREDICTIVE OPTIMIZATION;
```

> **Disable-then-enable precedence:** disable PO at the catalog/schema level *before* enabling at the account level and it stays **blocked** for those objects — an explicit child setting beats parent inheritance. (Disabling at the account level does not disable it for objects that explicitly enabled it.)

Verify with `DESCRIBE (CATALOG | SCHEMA | TABLE) EXTENDED name` (the *Predictive Optimization* field shows whether it's inherited).

## Observability & limitations

Observability via the system table `system.storage.predictive_optimization_operations_history` (operations, costs, impact). PO does **not** run on OpenSharing-recipient tables or **external tables**.

Related: [[managed-tables]], [[ch02-managing-data-with-delta-lake]], [[optimize-data-workloads-guide]], [[liquid-clustering]], [[catalog-commits]].
