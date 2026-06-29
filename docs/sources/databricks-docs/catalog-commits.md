# Catalog commits

> **Source:** [docs.databricks.com/aws/en/tables/features/catalog-commits](https://docs.databricks.com/aws/en/tables/features/catalog-commits)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-23
> **Tags:** tables, unity-catalog, managed, delta, iceberg, catalog-commits, transactions, catalogManaged, external-access, streaming, opensharing, B4
> **Type:** documentation

Catalog commits is a **Delta Lake table feature** that moves commit coordination **from the file system to Unity Catalog**, making the catalog the single source of truth for table state. Traditional Delta coordinates commits per-table (each table owns its log + conflict detection); catalog commits hoist that to the **catalog level** so UC can govern all access, orchestrate commits **across multiple tables in one transaction**, and serve table metadata directly (skipping cloud storage). ACID guarantees are preserved. It's the substrate behind multi-table [[transactions]] — **catalog commits is the coordination layer; multi-statement transactions are what it unlocks.** Enable it with the `delta.feature.catalogManaged` table property (off by default).

> "Catalog commits move this coordination to the catalog level. This allows organizations to consistently govern all access to the Lakehouse through Unity Catalog. It also allows Unity Catalog to orchestrate commits across multiple tables within a single transaction boundary while maintaining Delta Lake's ACID guarantees."

Requirements: UC **managed** tables only (Delta or Iceberg); **DBR 16.4+** to read/write/create catalog-commits tables, **DBR 18.0+** to enable/disable on existing tables.

## Benefits

| Benefit | Mechanism |
|---|---|
| **Transactions spanning multiple tables** | Multiple SQL statements across multiple tables = one atomic commit; all succeed or all fail. (→ [[transactions]]) |
| **Governed access** | Reads/writes coordinated through UC → engines always see latest committed state, governance policies applied |
| **Faster query planning & writes** | UC serves table-level metadata **directly** to the Delta client on access — skips cloud storage, removing a major metadata-latency source |
| **Enforceable constraints** | UC validates/rejects schema + constraint changes, blocking incompatible updates that break integrity or downstream jobs |
| **External access** *(Beta)* | External engines safely write to UC managed tables; UC coordinates commits to prevent corruption + concurrency conflicts |

> "Unity Catalog informs a Delta client of table-level metadata directly when it accesses a table, skipping cloud storage and removing a major source of metadata latency." The speed win is UC acting as a metadata cache so the client never round-trips cloud storage to learn table state.

## Preview/maturity status (three different gates)

- Writes to UC managed **Delta** tables via transactions → **Public Preview**.
- Writes to UC managed **Iceberg** tables via transactions → **Private Preview** (managed Iceberg enrollment form).
- **External access** to catalog-commits tables → **Beta**, controlled per workspace on the Previews page.

## Enable

**New table** — set `delta.feature.catalogManaged` at create time:

```sql
CREATE TABLE sales_data (
  sale_id BIGINT,
  amount DECIMAL(10,2),
  sale_date DATE
)
TBLPROPERTIES ('delta.feature.catalogManaged' = 'supported');
```

**Existing table** — `ALTER TABLE sales_data SET TBLPROPERTIES ('delta.feature.catalogManaged' = 'supported');`

> ⚠️ Enabling on an existing table **synchronizes table state with the catalog** — can take **several minutes** on tables with high write workloads.

Check with `DESCRIBE DETAIL sales_data` → `catalogManaged` appears in the `tableFeatures` column when enabled.

## Disable

DBR 18.0+ only, via drop-table-feature + protocol downgrade.

> ⚠️ **Do not cancel an upgrade/downgrade mid-`ALTER`/`DROP`.** Interruption can leave the table **partially upgraded/downgraded and locked from all reads and writes**. To revert, **re-run the command** — do not cancel. If the table locks, contact Databricks support.

## Limitations

- Cannot enable/disable on existing tables via `CREATE OR REPLACE TABLE` / `REPLACE TABLE` — use `CREATE TABLE` (with the property) at creation, or `ALTER TABLE` to toggle.
- **Streaming tables** need account-team access to the Public Preview.
- **Incompatible with external data access on streaming tables** — must disable external access first.
- Tables with catalog commits are shared through **OpenSharing using pre-signed URLs** instead of cloud tokens.
- **Materialized views cannot** have catalog commits.
- **Single-user clusters cannot** access streaming tables with catalog commits enabled.

Related: [[transactions]], [[managed-tables]], [[tables-concepts]], [[convert-external-managed]], [catalog-commits write mechanics (SunnyData)](../sunnydata/catalog-commits/).
