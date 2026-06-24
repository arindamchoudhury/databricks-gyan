# Predictive optimization for Unity Catalog managed tables

> **Source:** [docs.databricks.com/aws/en/optimizations/predictive-optimization](https://docs.databricks.com/aws/en/optimizations/predictive-optimization)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-18
> **Tags:** tables, unity-catalog, managed, delta, iceberg, predictive-optimization, optimize, vacuum, analyze, liquid-clustering, serverless, system-tables, B4, B5
> **Type:** documentation

## Summary
Predictive optimization automatically runs `OPTIMIZE`, `VACUUM`, and `ANALYZE` on Unity Catalog **managed** tables (Delta Lake and Iceberg), removing manual maintenance. Databricks identifies tables that benefit from maintenance, queues the operations, and collects statistics on write. Enabled by default for accounts created on or after **Nov 11, 2024**; existing accounts roll out through **August 2026**. Runs on serverless jobs compute (billed to a serverless jobs SKU). Databricks recommends it for **all** managed tables.

## Key points

- Three operations, all on UC managed tables only: `OPTIMIZE`, `VACUUM`, `ANALYZE`.
- Default-on for new accounts (≥ Nov 11 2024); gradual rollout to existing accounts completes by Aug 2026.
- Inheritance model: account → catalog → schema → table. Override at catalog or schema level.
- `OPTIMIZE` here does **not** run `ZORDER`; Z-ordered files are ignored. Targets liquid clustering / file-size compaction instead.
- `VACUUM` retention = `delta.deletedFileRetentionDuration` (default **7 days**). Raise it **before** enabling PO if you need longer time travel.
- Runs on **serverless compute for jobs** — billed via serverless jobs SKU.
- Observability via system table `system.storage.predictive_optimization_operations_history`.
- Does **not** run on external tables or OpenSharing-recipient tables.

## Notes

### What operations it runs

| Operation | What PO does |
|---|---|
| `OPTIMIZE` | Triggers incremental clustering for enabled tables; improves query perf by optimizing file sizes. |
| `VACUUM` | Reduces storage cost by deleting data files no longer referenced by the table. |
| `ANALYZE` | Incremental update of statistics to improve query performance. |

Two automatic behaviors when enabled:

1. Identifies tables that would benefit from maintenance and **queues** those operations.
2. Collects statistics when data is **written** to a managed table.

> **OPTIMIZE caveat:** `OPTIMIZE` does **not** run `ZORDER` when executed by predictive optimization. On Z-order tables, PO **ignores** Z-ordered files. If automatic liquid clustering is enabled, PO might select new clustering keys before clustering data.

### VACUUM retention warning

The retention window is the `delta.deletedFileRetentionDuration` table property (default **7 days**). `VACUUM` removes unreferenced data files within that window. To keep data longer (e.g. extended time travel), set this **before** enabling predictive optimization:

```sql
ALTER TABLE table_name SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = '30 days');
```

### Compute and billing

PO runs `ANALYZE`, `OPTIMIZE`, `VACUUM` on **serverless compute for jobs**. Billed to a serverless jobs SKU. Track cost/impact via the system table (below).

### Prerequisites

- Workspace on **Premium plan or above** in a supported region.
- **SQL warehouses** or **Databricks Runtime 12.2 LTS or above**.
- Only **Unity Catalog managed tables** are supported.

### Enable / disable (inheritance model)

Enable for an account, catalog, or schema. All UC managed tables inherit the **account** value by default; override at catalog or schema.

Required privileges:

| UC object | Privilege |
|---|---|
| Account | Account admin |
| Catalog | Catalog owner |
| Schema | Schema owner |

**Account level:** accounts console → Settings → Feature enablement → set *Predictive optimization*.

- Metastores in unsupported regions aren't enabled.
- Disabling at the account level does **not** disable it for catalogs/schemas that explicitly enabled it.

**Catalog / schema level** — `ENABLE | DISABLE | INHERIT`:

```sql
ALTER CATALOG [catalog_name] { ENABLE | DISABLE | INHERIT } PREDICTIVE OPTIMIZATION;
ALTER { SCHEMA | DATABASE } schema_name { ENABLE | DISABLE | INHERIT } PREDICTIVE OPTIMIZATION;
```

> **Disable-then-enable precedence:** You can disable PO at the catalog/schema level *before* enabling it at the account level. If the account later enables PO, it stays **blocked** for those objects. Explicit child setting beats parent inheritance.

### Verify whether enabled

The *Predictive Optimization* field is a UC property; if inherited from a parent, the value indicates so.

```sql
DESCRIBE (CATALOG | SCHEMA | TABLE) EXTENDED name
```

### Observability — system table

`system.storage.predictive_optimization_operations_history` gives operations, costs, and impact. See "Predictive optimization system table reference."

### Limitations

PO does **not** run on:

- Tables loaded to a workspace as **OpenSharing recipients**.
- **External tables**.

## Quotes worth keeping

> "Predictive optimization is enabled by default for accounts created on or after November 11, 2024. ... This rollout is expected to complete by August 2026." (NOTE, top of page)

> "OPTIMIZE does not run ZORDER when executed by predictive optimization. On tables that use Z-order, predictive optimization ignores Z-ordered files." (Operations NOTE)

## Open questions

- Iceberg managed tables are in scope — does `VACUUM`/retention behave identically to Delta, or via Iceberg snapshot expiry? Page treats them uniformly but only gives the Delta `delta.deletedFileRetentionDuration` property.
- What heuristics decide a table "would benefit" from maintenance? Page says "identifies" but not the signals.

## Related sources

- [[managed-tables]] — feature table lists PO as a managed-table capability; this page is the deep dive on the same feature. Confirms recommendation to enable for all managed tables.
- [[ch02-managing-data-with-delta-lake]] — manual `OPTIMIZE` / `VACUUM` / liquid clustering / Z-order mechanics that PO automates.
- [[optimize-data-workloads-guide]] — the manual-tuning counterpart: when you'd still reach for explicit `OPTIMIZE`/`VACUUM`/Z-order vs letting PO handle it.
- [[catalog-commits]] — managed-table commit model these maintenance ops write through.
