# Ch 2 — Managing Data with Delta Lake

> **Source:** Derar Alhussein, *Databricks Certified Data Engineer Associate Study Guide* (O'Reilly, 1st Ed., Feb 2025) — Chapter 2, PDF pp. 114–168.
> **Companion notebook:** `Chapter 2 - Managing Data with Delta Lake/2.1 - Delta Lake.sql` — every cell maps 1:1 to the hands-on sections below (§5–§9).
> **Added:** 2026-06-19
> **Tags:** delta-lake, transaction-log, acid, time-travel, optimize, vacuum, liquid-clustering, deletion-vectors, B5
> **Type:** book

> *Delta Lake from first principles: the transaction log architecture, the four ACID scenarios, hands-on table DDL, time travel + rollback, compaction with OPTIMIZE/Z-Order, and VACUUM for storage cleanup.*

> 📌 **Notes adapted to the 2026 platform.** The book targets DBR 13.3 LTS. Key shifts for this chapter flagged with ⚠️: (1) **Liquid Clustering** is now the Databricks-recommended replacement for Z-Order/partitioning (GA on DBR 15.4 LTS+; `CLUSTER BY AUTO` lets the platform pick keys); (2) **Deletion Vectors** (default-enabled since DBR 14.0+) change how UPDATE/DELETE work under the hood; (3) the book uses `hive_metastore` but **Unity Catalog is the default** in all new 2026 workspaces — stored at `__unitystorage`, not `dbfs:/user/hive/warehouse/`; (4) **Predictive Optimization** now runs `OPTIMIZE` / `VACUUM` / `ANALYZE` *automatically* on UC managed tables — the manual maintenance commands in §7–§8 are still valid but increasingly the platform's job, not yours. See [research-cache](../../research-cache/dcde-sg-ch02-facts.md).

> 📎 **Overlaps:** personal book chapter [[ch05-delta-lake]] covers the same ground with deeper explanatory treatment.

---

## 1. What Is Delta Lake?

Delta Lake is an **open-source storage layer** that sits *on top of* a data lake. It is not a storage medium or storage format — Parquet is the format; Delta Lake is the framework that manages it.

Why it exists: traditional data lakes lack ACID transactions → partially committed data, corrupted files, no consistent reads. Delta Lake fixes this.

Three defining properties:
- **ACID transactions** on cloud object storage.
- **Open source** — source code on GitHub, not proprietary.
- **Cloud-agnostic** — integrates with S3, ADLS, GCS.

> 💡 Exam framing: "Delta Lake is not a storage format." It runs *on top of* Parquet files. The lakehouse = Delta Lake + cloud storage.

---

## 2. The Delta Transaction Log (Delta Log)

The transaction log is the heart of Delta Lake. Every Delta table has a `_delta_log/` subdirectory alongside its Parquet data files.

**Structure:**
- Each committed transaction → one JSON file in `_delta_log/` (e.g., `000.json`, `001.json`).
- JSON file records: operation type, predicate/filters used, names of files **added**, names of files **removed** (soft-deleted).
- Associated `.crc` checksum files verify each JSON's integrity.

**Role:**
- Source of truth for table state and history.
- Every query hits the log *first* to determine which Parquet files are valid in the current version.
- Enables ACID: a write only "commits" when its JSON log entry is written; an incomplete write produces a Parquet file that never appears in the log → queries never see it.

**Checkpoint files:** at every 10 committed versions, Delta writes a `.checkpoint.parquet` that consolidates the log so Spark doesn't have to replay all JSON files from the beginning. (Book doesn't cover this; exam occasionally mentions it.)

---

## 3. How Delta Lake Guarantees ACID — Four Scenarios

The book walks through Alice (producer) and Bob (consumer) on the same table across four scenarios. These scenarios illustrate all four ACID properties in practice.

### 3.1 Write + Read (Atomicity / Durability)

1. Alice creates the table → Delta writes `part1.parquet`, `part2.parquet`, then writes `000.json` to the log.
2. Bob queries → Delta reads `000.json` first, then reads `part1` + `part2`.
3. If Alice's write had failed mid-way, no `000.json` would exist → Bob's query sees nothing. Guarantees **atomicity** (all or nothing).

### 3.2 Update (Immutability)

Parquet files are **immutable** — Delta never edits an existing file.

Update flow:
1. Alice updates a record in `part1.parquet`.
2. Delta copies the relevant rows from `part1` → applies the change → writes `part3.parquet`.
3. Delta writes `001.json`: marks `part1` as **removed**, marks `part3` as **added**.
4. Bob reads the log → sees only `part2` + `part3`; `part1` is invisible.

`part1` remains on storage as an obsolete file until `VACUUM` cleans it up. This is what enables **time travel**.

> ⚠️ **2026 update — Deletion Vectors:** Starting DBR 14.0, UPDATE and DELETE no longer copy files by default. Instead, Delta writes a **deletion vector** — a bitmap file that marks which rows in the original Parquet file are stale. Reads merge the Parquet file with its deletion vector on the fly. This eliminates write amplification for point updates/deletes and enables **row-level concurrency** (DBR 14.2+). The book's file-copy model is correct for the pre-DV world; the *logical result* is identical, only the physical mechanism differs.

### 3.3 Concurrent Write + Read (Isolation)

While Alice is writing `part4.parquet` (not yet committed), Bob queries. The log only references `part2` + `part3` — Bob reads those. No deadlock, no wait. Bob gets a **consistent snapshot** of the committed state.

Once Alice's write finishes, Delta appends `002.json` marking `part4` as added.

### 3.4 Failed Write (Consistency)

Alice starts writing `part5.parquet`; an error occurs mid-write. The incomplete file exists on storage but **no log entry** is ever written. Bob queries → reads the log → `part5` is invisible. Bob is protected from dirty/incomplete data.

---

## 4. Delta Lake Advantages (from the transaction log)

| Advantage | What it means |
|---|---|
| **ACID transactions** | Atomic + consistent data ops; no partial commits. |
| **Scalable metadata handling** | Table metadata lives in the log alongside the data, not in a slow centralized metastore. Enables efficient large-directory listings. Includes table statistics to accelerate query planning. |
| **Full audit logging** | Every operation (insert, update, delete, optimize…) recorded with timestamp + user info → supports governance and troubleshooting. |

---

## 5. Working with Delta Lake Tables — Hands-On

### 5.1 Creating Tables

```sql
-- USING DELTA is optional — Delta is the Databricks default
CREATE TABLE product_info (
    product_id   INT,
    product_name STRING,
    category     STRING,
    price        DOUBLE,
    quantity     INT
)
USING DELTA;
```

> ⚠️ **2026 — Unity Catalog default:** The book uses `USE CATALOG hive_metastore` to simplify the demo. In real 2026 workspaces, Unity Catalog is the default; tables land in `__unitystorage` (managed by UC) rather than `dbfs:/user/hive/warehouse/`. The `%fs ls` and `DESCRIBE DETAIL` paths shown in the book won't work against UC-managed tables without extra permissions. Use UC catalog/schema for new work; the `hive_metastore` shortcut is fine for local practice.

### 5.2 Inserting Data

```sql
INSERT INTO product_info (product_id, product_name, category, price, quantity)
VALUES (1, 'Winter Jacket', 'Clothing', 79.95, 100);

INSERT INTO product_info (product_id, product_name, category, price, quantity)
VALUES
  (2, 'Microwave',  'Kitchen',     249.75,  30),
  (3, 'Board Game', 'Toys',         29.99,  75),
  (4, 'Smartcar',   'Electronics', 599.99,  50);
```

Each `INSERT` = one transaction = one Parquet file + one JSON log entry. Two INSERTs → two files, two log entries.

> 💡 Tip: running two SQL statements in the same cell shows only the last result. To see both, use separate cells or select + `Shift+Ctrl+Enter`.

### 5.3 Exploring the Table Directory

```sql
DESCRIBE DETAIL product_info
-- → numFiles: 2, location: dbfs:/user/hive/warehouse/product_info
```

```python
%fs ls 'dbfs:/user/hive/warehouse/product_info'
# Shows: part-*.parquet files + _delta_log/ subdirectory
```

### 5.4 Updating Tables

```sql
UPDATE product_info SET price = price + 10 WHERE product_id = 3
```

After the update, `DESCRIBE DETAIL` still shows `numFiles: 2` — not 3 — because the log references only the two *current* files (the updated copy + the untouched file). The original file for `product_id=3` is soft-deleted in the log.

### 5.5 Exploring Table History

```sql
DESCRIBE HISTORY product_info
```

Returns versions in reverse-chronological order with timestamp, operation type, `operationParameters` (predicates used), and user info.

Each `DESCRIBE HISTORY` row = one JSON file in `_delta_log/`.

```python
%fs head 'dbfs:/user/hive/warehouse/product_info/_delta_log/00000000000000000003.json'
# → {"commitInfo": {"operation": "UPDATE", ...}}
#    {"add":    {"path": "part-...-c000.snappy.parquet", ...}}
#    {"remove": {"path": "part-...-c000.snappy.parquet", "deletionTimestamp": ...}}
```

---

## 6. Time Travel

Delta's versioning is automatic — every write increments the version. No configuration needed.

### 6.1 Querying Older Versions

**By version:**
```sql
SELECT * FROM product_info VERSION AS OF 2
SELECT * FROM product_info@v2   -- shorthand
```

**By timestamp:**
```sql
SELECT * FROM product_info TIMESTAMP AS OF '2024-02-25 12:00:00'
```

Version 0 = table creation (empty schema only, no data); Versions 1/2 = the two INSERTs; Version 3 = the UPDATE.

### 6.2 Rolling Back (RESTORE TABLE)

```sql
-- Accidentally deleted all rows:
DELETE FROM product_info   -- becomes version 4

-- Restore to version 3:
RESTORE TABLE product_info TO VERSION AS OF 3
-- → new version 5 recorded in history
```

`RESTORE TABLE` is **non-destructive** — it creates a new version rather than erasing history.

> 💡 Exam: `RESTORE TABLE` is the correct command for rollback. `DROP TABLE` is destructive and permanent. Time travel only works if the underlying Parquet files haven't been vacuumed yet.

---

## 7. Optimizing Delta Lake Tables

### 7.1 OPTIMIZE (Compaction)

Small files accumulate from many incremental writes. `OPTIMIZE` compacts them into larger files (target ~1 GB), improving read performance.

```sql
OPTIMIZE product_info
```

Files compacted → old files soft-deleted in log → `numFiles` drops. The compaction is recorded as a new table version.

### 7.2 Z-Order Indexing

Z-Order co-locates related data within compacted files by column value, enabling **data skipping** at scan time.

```sql
OPTIMIZE product_info ZORDER BY product_id
-- Rows with product_id 1–50 cluster in file 1; 51–100 in file 2
-- Query for product_id = 25 → only file 1 scanned
```

> ⚠️ **2026 recommendation — Liquid Clustering:** Databricks now recommends **Liquid Clustering** over Z-Order (and over Hive partitioning) for all new tables. Differences:
>
> | | Z-Order | Liquid Clustering |
> |---|---|---|
> | How set | `OPTIMIZE … ZORDER BY` | `CLUSTER BY (col)` at table creation |
> | Incremental? | No — full rewrite each run | Yes — only new data reclustered |
> | Change keys later? | Must recreate table | `ALTER TABLE … CLUSTER BY (new_col)` |
> | Write amplification | High (non-incremental) | ~7× lower than partition+ZOrder |
>
> ```sql
> -- Create with liquid clustering (2026 pattern):
> CREATE TABLE product_info (...)
> CLUSTER BY (product_id);
>
> -- Or let the platform choose keys (DBR 15.4 LTS+, UC managed only):
> CREATE TABLE product_info (...)
> CLUSTER BY AUTO;
>
> -- Still run OPTIMIZE to trigger clustering (or let Predictive Optimization do it):
> OPTIMIZE product_info
> ```
>
> **Auto liquid clustering** (`CLUSTER BY AUTO`, GA DBR 15.4 LTS+): predictive optimization picks and adapts clustering keys from observed query patterns; UC managed tables only. `ALTER TABLE t CLUSTER BY AUTO` enables it on an existing table.
>
> Z-Order remains valid for existing tables and the DCDEA exam still tests it, but note **predictive optimization's `OPTIMIZE` never runs `ZORDER`** and ignores Z-ordered files — another reason Z-Order is legacy. Use Liquid Clustering for any new table; GA is **DBR 15.4 LTS+** (14.3 LTS supported it via DataFrame/DeltaTable API only).

---

## 8. Vacuuming

`VACUUM` deletes Parquet files that are no longer referenced by the transaction log and are older than the retention threshold.

```sql
VACUUM product_info                  -- default: remove files older than 7 days
VACUUM product_info RETAIN 168 HOURS -- explicit 7-day retention
```

**The retention trade-off:**
- Files deleted by VACUUM cannot be recovered.
- Time travel only works for versions whose underlying files still exist.
- Vacuuming past a version means you can no longer `SELECT … VERSION AS OF <that-version>`.

**Safety check:** Delta refuses `RETAIN 0 HOURS` by default:
```
IllegalArgumentException: requirement failed: Are you sure you want to vacuum files with
such a low retention period? If you have writers that are currently writing to this table,
there is a risk that you may corrupt the state of your Delta table.
```

Override for demos only (not production):
```sql
SET spark.databricks.delta.retentionDurationCheck.enabled = false;
VACUUM product_info RETAIN 0 HOURS
```

> 💡 Exam: **7 days** is the default VACUUM retention. VACUUM affects time travel reach. VACUUM does **not** create a new table version — it just deletes physical files.

> ⚠️ **2026 — Predictive Optimization runs VACUUM for you.** On UC managed tables, predictive optimization auto-runs `VACUUM` (and `OPTIMIZE`/`ANALYZE`) on serverless compute, billed at a serverless jobs SKU. The retention window is the table property `delta.deletedFileRetentionDuration` (default 7 days) — to keep longer time travel, raise it *before* enabling PO:
> ```sql
> ALTER TABLE product_info SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 30 days');
> ```
> Default-on for accounts created on/after 2024-11-11; existing-account rollout completing ~Aug 2026. UC managed tables only (not external, not `hive_metastore`).

---

## 9. Dropping Tables

```sql
DROP TABLE product_info
-- Removes table + data directory entirely (for non-UC managed tables)
```

Attempting to query or `%fs ls` after DROP raises `FileNotFoundException`.

---

## 10. Summary

| Command | What it does |
|---|---|
| `DESCRIBE DETAIL` | Table metadata: `numFiles`, location, format, schema |
| `DESCRIBE HISTORY` | Ordered log of all versions with operation + timestamp |
| `SELECT … VERSION AS OF n` / `@vN` | Time travel by version |
| `SELECT … TIMESTAMP AS OF ts` | Time travel by timestamp |
| `RESTORE TABLE … TO VERSION AS OF n` | Roll back to a prior version (new version created) |
| `OPTIMIZE` | Compact small files into larger ones |
| `OPTIMIZE … ZORDER BY col` | Compact + co-locate data by column for data skipping |
| `VACUUM [RETAIN n HOURS]` | Delete obsolete files older than threshold (default 7d) |

---

## Sample Exam Questions (from book)

**Q1 — Conceptual:** Which statement best describes Delta Lake time travel?
→ **E.** It allows users to query Delta Lake tables at a specific point in time, providing views of previous states of the data.

**Q2 — Code:** A Delta table has too many small files causing slow reads. Which command fixes it?
→ **B.** `OPTIMIZE customer_orders`

(Z-ORDER alone doesn't compact; VACUUM removes obsolete files but doesn't compact; RESTORE rolls back data.)

---

## References

- Delta transaction log deep-dive: <https://www.databricks.com/blog/2019/08/21/diving-into-delta-lake-unpacking-the-transaction-log.html>
- Liquid clustering (GA announcement): <https://www.databricks.com/blog/announcing-general-availability-liquid-clustering>
- Deletion vectors: <https://docs.databricks.com/aws/en/delta/deletion-vectors>
- OPTIMIZE docs: <https://docs.databricks.com/aws/en/sql/language-manual/delta-optimize>
