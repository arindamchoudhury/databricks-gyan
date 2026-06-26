# Transactions

> **Source:** [docs.databricks.com/aws/en/transactions/](https://docs.databricks.com/aws/en/transactions/)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-23
> **Tags:** tables, unity-catalog, transactions, acid, catalog-commits, isolation, concurrency, multi-statement, atomic, rollback, opensharing, B4
> **Type:** documentation

## Summary

Transactions coordinate operations **across multiple SQL statements and multiple tables** as one atomic unit — all changes commit together or roll back together, with full ACID. This is the **capability that [[catalog-commits]] enables**: every table written in a transaction must be a UC managed table with catalog commits (`catalogManaged`) on. Two modes: **non-interactive** (`BEGIN ATOMIC … END`, auto-commit/rollback, row-level concurrency — the recommended default) and **interactive** (`BEGIN TRANSACTION; … COMMIT;`, manual, table-level concurrency, for conditional logic + JDBC/ODBC clients). Uses **optimistic concurrency** (no locks; conflicts detected at commit). Each transaction = **one Delta log entry** regardless of statement count.

## Key points

- **What:** atomic coordination across multiple statements + tables; ACID; all-or-nothing.
- **Maturity:** Delta = **Public Preview**, Iceberg = **Private Preview**.
- **Hard requirement:** all written tables = UC **managed** (Delta/Iceberg) with **catalog commits enabled** ([[catalog-commits]]). DML only — **no DDL inside transactions**.
- **Two modes:** non-interactive `BEGIN ATOMIC…END` (auto, row-level concurrency) vs interactive `BEGIN TRANSACTION;…COMMIT;` (manual, table-level). Databricks recommends **non-interactive** for most cases.
- **Compute:** non-interactive → any SQL warehouse / serverless / **DBR 18.0+** cluster; interactive → **any SQL warehouse**; OpenSharing shared assets → **DBR 18.1+**.
- **Isolation:** repeatable reads via a **consistent snapshot captured at first access** to each table.
- **Concurrency:** optimistic; conflicts caught at commit. Non-interactive supports **row-level** concurrency; interactive only **table-level**.
- **Hard limits:** ≤100 tables read+write combined, ≤100 views read, ≤100 intermediate commits per table; auto-rollback after **48 h** total (interactive also **10 min** idle); **no streaming writes, no time travel, no RLS/CLM tables**.

## Notes

### Example transaction

```sql
-- Non-interactive
BEGIN ATOMIC
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
  INSERT INTO audit_log VALUES (1, 2, 100, current_timestamp());
END;
```

All three commit together; any failure → all roll back, transaction terminated without side effects. Usable with stored procedures + SQL Scripting for warehousing workloads.

### Requirements

For transactions spanning multiple statements/tables, **every table written** must:

- be a **UC managed table** (Delta or Iceberg),
- have **catalog commits enabled** ([[catalog-commits]]).

Plus supported compute:

| Transaction type | Compute |
|---|---|
| Non-interactive | any SQL warehouse, serverless, or **DBR 18.0+** cluster |
| Interactive | any SQL warehouse |
| On OpenSharing shared assets | **DBR 18.1+** |

### Transaction modes

| Mode | Syntax | Commit | Rollback | Best for |
|---|---|---|---|---|
| **Non-interactive** | `ATOMIC` compound statement | auto on success | auto on error | fixed sequences, scheduled jobs |
| **Interactive** | `BEGIN TRANSACTION; … COMMIT;` | manual | manual | conditional logic, validation/debugging, JDBC/ODBC/PyDBC |

### Supported operations

DML only inside a transaction: `SELECT` (subselect), `VALUES`, `INSERT` (all variants), `UPDATE`, `COPY INTO`, `DELETE FROM`, `MERGE INTO`.

### Read sources

Can read from UC tables (Delta + Iceberg), streaming tables, views, materialized views. For **non-transactional** sources (Parquet, Avro, federated JDBC) use the `allow_nontransactional_reads` hint:

```sql
BEGIN TRANSACTION;
INSERT INTO transactional_table
SELECT col1, col2
FROM parquet.`/path/to/data`
WITH (allow_nontransactional_reads = true);
-- managed Delta needs no hint
INSERT INTO another_table SELECT * FROM managed_delta_table;
COMMIT;
```

> ⚠️ Non-transactional reads are **not repeatable** — concurrent source changes during the transaction can give inconsistent reads.

### Isolation — snapshot at first access

Repeatable reads: first access to a table captures a **consistent snapshot**; all later reads of that table use it, even if others modify the table concurrently. Example: two `SELECT`s of `product_id = 1001` in one transaction both return the **original** row even if another session `UPDATE`s it between them.

### Conflict detection & concurrency

Optimistic concurrency — no locking; conflicts detected **at commit**. On conflict the transaction fails. Non-interactive rolls back automatically; interactive needs an explicit `ROLLBACK` to clear state before the next transaction.

- **Non-interactive** → row-level concurrency (two txns can modify different rows in the same file without conflict, if row-level concurrency enabled on targets).
- **Interactive** → table-level concurrency.

**Conflict scenarios:**

| Scenario | Description |
|---|---|
| Write-write | Two txns update/delete the same rows |
| Write-read | Another txn modified rows yours read — **Serializable only** |
| Phantom read | Another txn added rows matching a predicate yours read — **WriteSerializable + Serializable** |
| Metadata | Another txn changed schema or properties |

### How a transaction appears in the Delta log

Each successful transaction = **one Delta log entry** regardless of statement count → clean audit trail, simpler rollback. Individual operations are kept as **JSON metadata inside** that single log entry.

> Connects to [[ch02-managing-data-with-delta-lake]]'s transaction-log model: normally one commit = one statement; here one commit wraps N statements, with per-statement detail nested in the entry's JSON.

### Error handling & rollback

| Scenario | Non-interactive | Interactive |
|---|---|---|
| Statement failure | immediate auto-rollback | must run `ROLLBACK` (if session alive) |
| Failed validation/business rule | `SIGNAL` to throw → auto-rollback | run `ROLLBACK` |
| Session disconnect | auto-rollback | auto-rollback |
| Timeout | auto-rollback after **48 h** total | auto-rollback after **10 min idle** or **48 h** total; then `ROLLBACK` to clear state |

### Clients

- **SQL Editor / notebooks:** `BEGIN ATOMIC…END;` or `BEGIN TRANSACTION;…COMMIT;` in SQL cells, or `spark.sql()` in Python/Scala.
- **JDBC:** `setAutoCommit(false)`, `commit()`, `rollback()` — driver **3.0.5+**.
- **ODBC:** Databricks ODBC driver **2.10.0+**.
- **Python:** Databricks SQL Connector with `autocommit=False`.
- **Statement Execution API:** run via SQL syntax through API calls.

### Limitations (the long list)

- **Write targets:** only UC managed Delta/Iceberg with `catalogManaged` enabled.
- **DML only** — run DDL (`CREATE`/`ALTER`/`DROP TABLE`) outside transactions.
- **No metadata operations** inside (regardless of protocol): JDBC `DatabaseMetaData`, ODBC catalog functions, `SHOW TABLES/DATABASES`, `DESCRIBE TABLE`, and `SELECT` on `information_schema` / system tables.
- **Interactive conflicts** are coarser — table-level except `INSERT` that doesn't read the target. Use non-interactive when row-level matters.
- **COPY INTO concurrency:** a txn's `COPY INTO` fails if another concurrent `COPY INTO` writes the same table and commits first.
- **No streaming writes.**
- **No RLS/CLM** — tables with row filters or column masks can't participate.
- **Limits:** ≤100 tables (read+write combined), ≤100 views read, ≤100 intermediate commits per table.
- **No time travel** inside a transaction.
- **Lineage** is emitted as each read/write occurs and **persists even if rolled back**.
- **OpenSharing:** providers must share `WITH HISTORY` for recipients to transact; Databricks recipients limited to shared views/MVs/streaming tables/non-Iceberg foreign tables; same-account recipients need shared/serverless compute, cross-account need serverless; can't reference a shared view + shared table backed by the same source in one txn.

## Quotes worth keeping

> "Each successful transaction appears as a single entry in the table's Delta log, regardless of how many individual statements ran within the transaction. … Individual operations within a transaction are available as JSON metadata in the Delta log entry for the transaction." (How transactions appear in the Delta log)

> "When you access a table in a transaction, Databricks captures a consistent snapshot of that table at first access. All subsequent reads of that table use this snapshot." (Transaction isolation)

## Open questions

- The page lists WriteSerializable vs Serializable as affecting which conflicts fire (write-read = Serializable only; phantom = both) but defers isolation-level *selection* to "Transaction modes" — how you pick the level per transaction isn't on this page.

## Related sources

- [[catalog-commits]] — the enabling feature; every transaction write-target needs `catalogManaged`. This page is the capability that page's multi-table benefit pointed to.
- [[managed-tables]] — lists multi-statement transactions in the managed-only feature set; this is the full spec.
- [[ch02-managing-data-with-delta-lake]] — Delta transaction-log + isolation-level (WriteSerializable/Serializable, optimistic concurrency) foundations this builds on.
- [[multi-statement-transactions]] — practitioner companion (SunnyData/Hubert Dudek): the `BEGIN ATOMIC` SQL surface, the `.mst.json` staged-commit file, the success-vs-rollback storage walkthrough, and the SQL-only / not-OLTP(Lakebase) / not-OSS-Spark boundaries.

## References

- [Transactions](https://docs.databricks.com/aws/en/transactions/) — this page
- Learning path: **B4 — Spark SQL & Relational Entities**
