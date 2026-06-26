# Transactions

> **Source:** [docs.databricks.com/aws/en/transactions/](https://docs.databricks.com/aws/en/transactions/)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-23
> **Tags:** tables, unity-catalog, transactions, acid, catalog-commits, isolation, concurrency, multi-statement, atomic, rollback, opensharing, B4
> **Type:** documentation

Transactions coordinate operations **across multiple SQL statements and multiple tables** as one atomic unit — all changes commit together or roll back together, with full ACID. This is the capability that [[catalog-commits]] enables: every table written in a transaction must be a UC managed table with catalog commits (`catalogManaged`) on, and it's **DML only** (no DDL inside a transaction). Maturity: Delta = **Public Preview**, Iceberg = **Private Preview**. Concurrency is **optimistic** (no locks; conflicts detected at commit), and each transaction is **one Delta log entry** regardless of statement count.

There are two modes — Databricks recommends **non-interactive** for most cases:

| Mode | Syntax | Commit | Rollback | Concurrency | Best for |
|---|---|---|---|---|---|
| **Non-interactive** | `BEGIN ATOMIC … END` | auto on success | auto on error | row-level | fixed sequences, scheduled jobs |
| **Interactive** | `BEGIN TRANSACTION; … COMMIT;` | manual | manual | table-level | conditional logic, validation/debugging, JDBC/ODBC/PyDBC |

## Example transaction

```sql
BEGIN ATOMIC
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
  INSERT INTO audit_log VALUES (1, 2, 100, current_timestamp());
END;
```

All three commit together; any failure → all roll back, transaction terminated without side effects. Usable with stored procedures + SQL Scripting for warehousing workloads.

## Requirements

Every table **written** in a transaction must be a **UC managed table** (Delta or Iceberg) with **catalog commits enabled** ([[catalog-commits]]). Plus supported compute:

| Transaction type | Compute |
|---|---|
| Non-interactive | any SQL warehouse, serverless, or **DBR 18.0+** cluster |
| Interactive | any SQL warehouse |
| On OpenSharing shared assets | **DBR 18.1+** |

## Supported operations

DML only: `SELECT` (subselect), `VALUES`, `INSERT` (all variants), `UPDATE`, `COPY INTO`, `DELETE FROM`, `MERGE INTO`.

## Read sources

Can read from UC tables (Delta + Iceberg), streaming tables, views, and materialized views. For **non-transactional** sources (Parquet, Avro, federated JDBC) use the `allow_nontransactional_reads` hint:

```sql
BEGIN TRANSACTION;
INSERT INTO transactional_table
SELECT col1, col2
FROM parquet.`/path/to/data`
WITH (allow_nontransactional_reads = true);
INSERT INTO another_table SELECT * FROM managed_delta_table;   -- managed Delta needs no hint
COMMIT;
```

> ⚠️ Non-transactional reads are **not repeatable** — concurrent source changes during the transaction can give inconsistent reads.

## Isolation — snapshot at first access

> "When you access a table in a transaction, Databricks captures a consistent snapshot of that table at first access. All subsequent reads of that table use this snapshot."

So two `SELECT`s of `product_id = 1001` in one transaction both return the **original** row even if another session `UPDATE`s it between them.

## Conflict detection & concurrency

Optimistic concurrency — no locking; conflicts detected **at commit**, on which the transaction fails. Non-interactive rolls back automatically; interactive needs an explicit `ROLLBACK` before the next transaction. Non-interactive supports **row-level** concurrency (two txns can modify different rows in the same file without conflict, if enabled on targets); interactive is **table-level**.

| Scenario | Description |
|---|---|
| Write-write | Two txns update/delete the same rows |
| Write-read | Another txn modified rows yours read — **Serializable only** |
| Phantom read | Another txn added rows matching a predicate yours read — **WriteSerializable + Serializable** |
| Metadata | Another txn changed schema or properties |

## How a transaction appears in the Delta log

> "Each successful transaction appears as a single entry in the table's Delta log, regardless of how many individual statements ran within the transaction. … Individual operations within a transaction are available as JSON metadata in the Delta log entry for the transaction."

This connects to [[ch02-managing-data-with-delta-lake]]'s transaction-log model: normally one commit = one statement; here one commit wraps N statements, with per-statement detail nested in the entry's JSON → clean audit trail, simpler rollback.

## Error handling & rollback

| Scenario | Non-interactive | Interactive |
|---|---|---|
| Statement failure | immediate auto-rollback | must run `ROLLBACK` (if session alive) |
| Failed validation/business rule | `SIGNAL` to throw → auto-rollback | run `ROLLBACK` |
| Session disconnect | auto-rollback | auto-rollback |
| Timeout | auto-rollback after **48 h** total | auto-rollback after **10 min idle** or **48 h** total; then `ROLLBACK` |

## Clients

- **SQL Editor / notebooks:** `BEGIN ATOMIC…END;` or `BEGIN TRANSACTION;…COMMIT;` in SQL cells, or `spark.sql()` in Python/Scala.
- **JDBC:** `setAutoCommit(false)`, `commit()`, `rollback()` — driver **3.0.5+**.
- **ODBC:** Databricks ODBC driver **2.10.0+**.
- **Python:** Databricks SQL Connector with `autocommit=False`.
- **Statement Execution API:** run via SQL syntax through API calls.

## Limitations

- **Write targets:** only UC managed Delta/Iceberg with `catalogManaged` enabled.
- **DML only** — run DDL (`CREATE`/`ALTER`/`DROP TABLE`) outside transactions.
- **No metadata operations** inside (any protocol): JDBC `DatabaseMetaData`, ODBC catalog functions, `SHOW TABLES/DATABASES`, `DESCRIBE TABLE`, and `SELECT` on `information_schema` / system tables.
- **Interactive conflicts** are coarser — table-level except `INSERT` that doesn't read the target. Use non-interactive when row-level matters.
- **COPY INTO concurrency:** a txn's `COPY INTO` fails if another concurrent `COPY INTO` writes the same table and commits first.
- **No streaming writes.** **No time travel** inside a transaction. **No RLS/CLM** — tables with row filters or column masks can't participate.
- **Limits:** ≤100 tables (read+write combined), ≤100 views read, ≤100 intermediate commits per table.
- **Lineage** is emitted as each read/write occurs and **persists even if rolled back**.
- **OpenSharing:** providers must share `WITH HISTORY` for recipients to transact; Databricks recipients limited to shared views/MVs/streaming tables/non-Iceberg foreign tables; same-account recipients need shared/serverless compute, cross-account need serverless; can't reference a shared view + shared table backed by the same source in one txn.

Related: [[catalog-commits]], [[managed-tables]], [[ch02-managing-data-with-delta-lake]], [[multi-statement-transactions]].
