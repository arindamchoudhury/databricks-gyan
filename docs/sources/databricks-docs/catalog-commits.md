# Catalog commits

> **Source:** [docs.databricks.com/aws/en/tables/features/catalog-commits](https://docs.databricks.com/aws/en/tables/features/catalog-commits)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-23
> **Tags:** tables, unity-catalog, managed, delta, iceberg, catalog-commits, transactions, catalogManaged, external-access, streaming, opensharing, B4
> **Type:** documentation

## Summary

Catalog commits is a **Delta Lake table feature** that moves commit coordination **from the file system to Unity Catalog**, making the catalog the single source of truth for table state. Traditional Delta coordinates commits per-table (each table owns its log + conflict detection); catalog commits hoist that to the **catalog level** so UC can govern all access, orchestrate commits **across multiple tables in one transaction**, and serve table metadata directly (skipping cloud storage). This is the enabling feature behind multi-table **Transactions** referenced in [[managed-tables]] — it answers that page's open question about how catalog commits relates to multi-statement transactions: **catalog commits is the substrate; multi-statement transactions are what it unlocks.** Enabled via the `delta.feature.catalogManaged` table property. Off by default.

## Key points

- **What it changes:** commit coordination moves from per-table transaction log → Unity Catalog (catalog becomes single source of truth). ACID guarantees preserved.
- **Enable:** set table property `delta.feature.catalogManaged = 'supported'` (on `CREATE TABLE`, or `ALTER TABLE` for existing).
- **Requirements:** UC **managed** tables only (Delta or Iceberg); **DBR 16.4+** to read/write/create catalog-commits tables; **DBR 18.0+** to enable/disable on existing tables.
- **External access is Beta**, gated on the Previews page (workspace admin controls it).
- **Multi-table transactions:** Delta = **Public Preview**, Iceberg = **Private Preview** (enrollment form).
- **Check:** `DESCRIBE DETAIL` → `catalogManaged` in the `tableFeatures` column.
- **Disable** needs DBR 18.0+ via drop-table-feature / protocol downgrade.

## Notes

### Why hoist commits to the catalog — the four benefits

| Benefit | Mechanism |
|---|---|
| **Transactions spanning multiple tables** | Multiple SQL statements across multiple tables = one atomic commit; all succeed or all fail. (→ Transactions) |
| **Governed access** | Reads/writes coordinated through UC → engines always see latest committed state, governance policies applied |
| **Faster query planning & writes** | UC serves table-level metadata **directly** to the Delta client on access — skips cloud storage, removes a major metadata-latency source |
| **Enforceable constraints** | UC validates/rejects schema + constraint changes, blocking incompatible updates that break integrity or downstream jobs |
| **External access** *(Beta)* | External engines safely write to UC managed tables; UC coordinates commits to prevent corruption + concurrency conflicts |

> Confirms [[managed-tables]]'s feature-table summary of catalog commits, and adds the *why*: the speed win is UC acting as a metadata cache so the client never round-trips cloud storage to learn table state.

### Preview/maturity status (read carefully — three different gates)

- Writes to UC managed **Delta** tables via transactions → **Public Preview**.
- Writes to UC managed **Iceberg** tables via transactions → **Private Preview** (managed Iceberg enrollment form).
- **External access** to catalog-commits tables → **Beta**, controlled per workspace on the Previews page.

### Enable

**New table** — `delta.feature.catalogManaged` at create time:

```sql
CREATE TABLE sales_data (
  sale_id BIGINT,
  amount DECIMAL(10,2),
  sale_date DATE
)
TBLPROPERTIES ('delta.feature.catalogManaged' = 'supported');
```

**Existing table** — `ALTER TABLE`:

```sql
ALTER TABLE sales_data SET TBLPROPERTIES ('delta.feature.catalogManaged' = 'supported');
```

> ⚠️ Enabling on an existing table **synchronizes table state with the catalog** — can take **several minutes** on tables with high write workloads.

**Check if enabled:**

```sql
DESCRIBE DETAIL sales_data;
-- if enabled, `catalogManaged` appears in the tableFeatures column
```

### Disable

DBR 18.0+ only. Use drop-table-feature + protocol downgrade.

> ⚠️ **Do not cancel an upgrade/downgrade mid-`ALTER`/`DROP`.** Interruption can leave the table **partially upgraded/downgraded and locked from all reads and writes**. To revert, **re-run the command** — do not cancel. If the table locks, contact Databricks support.

### Limitations

- Cannot enable/disable on existing tables via `CREATE OR REPLACE TABLE` / `REPLACE TABLE`. Use `CREATE TABLE` (with the property) to enable at creation, or `ALTER TABLE` to toggle on an existing table.
- **Streaming tables** need account-team access to the Public Preview.
- Catalog commits is **incompatible with external data access on streaming tables** — must disable external access first.
- Tables with catalog commits are shared through **OpenSharing using pre-signed URLs** instead of cloud tokens.
- **Materialized views cannot** have catalog commits.
- **Single-user clusters cannot** access streaming tables with catalog commits enabled.

## Quotes worth keeping

> "Catalog commits move this coordination to the catalog level. This allows organizations to consistently govern all access to the Lakehouse through Unity Catalog. It also allows Unity Catalog to orchestrate commits across multiple tables within a single transaction boundary while maintaining Delta Lake's ACID guarantees." (Overview)

> "Unity Catalog informs a Delta client of table-level metadata directly when it accesses a table, skipping cloud storage and removing a major source of metadata latency." (Benefits — Faster query planning and writes)

## Open questions

- Page says streaming-table support needs *account-team* access while general external access is a *Previews-page* Beta — two separate gating mechanisms; the page doesn't explain how they interact when a streaming table also needs external writes (and limitations say those two can't coexist anyway).

## Related sources

- [[transactions]] — the multi-table transaction capability this feature unlocks; every transaction write-target requires catalog commits. Full spec of `BEGIN ATOMIC`/`BEGIN TRANSACTION`, isolation, conflict detection, and limits.
- [[managed-tables]] — lists catalog commits in the unique-to-managed feature table and raises the open question (catalog commits vs multi-statement transactions) that **this page answers**: catalog commits is the coordination substrate; multi-statement transactions are the capability it enables.
- [[tables-concepts]] — defines the UC managed table type that catalog commits requires.
- [[convert-external-managed]] — external→managed conversion is a prerequisite path to even qualify for catalog commits (managed-only feature).

## References

- [Catalog commits](https://docs.databricks.com/aws/en/tables/features/catalog-commits) — this page
- Learning path: **B4 — Spark SQL & Relational Entities**
