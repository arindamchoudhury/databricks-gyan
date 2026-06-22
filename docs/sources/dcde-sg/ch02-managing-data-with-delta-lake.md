# Ch 2 — Managing Data with Delta Lake

> **Source:** Derar Alhussein, *Databricks Certified Data Engineer Associate Study Guide* (O'Reilly, 1st Ed., Feb 2025) — Chapter 2, PDF pp. 114–168.
> 
> **Companion notebook:** `Chapter 2 - Managing Data with Delta Lake/2.1 - Delta Lake.sql` — every cell maps 1:1 to the hands-on sections below (§5–§9).
> 
> **Added:** 2026-06-19
>
> **Tags:** delta-lake, transaction-log, acid, time-travel, optimize, vacuum, liquid-clustering, deletion-vectors, B5
> 
> **Type:** book

> *Delta Lake from first principles: the transaction log architecture, the four ACID scenarios, hands-on table DDL, time travel + rollback, compaction with OPTIMIZE/Z-Order, and VACUUM for storage cleanup.*

> 📌 **Notes adapted to the 2026 platform.** The book targets DBR 13.3 LTS. Key shifts for this chapter flagged with ⚠️: (1) **Liquid Clustering** is now the Databricks-recommended replacement for Z-Order/partitioning (GA on DBR 15.4 LTS+; `CLUSTER BY AUTO` lets the platform pick keys); (2) **Deletion Vectors** (default-enabled since DBR 14.0+) change how UPDATE/DELETE work under the hood; (3) the book uses `hive_metastore` but **Unity Catalog is the default** in all new 2026 workspaces — managed tables land in UC managed storage (e.g. `s3://<bucket>/__unity_storage/catalogs/<catalog_id>/tables/<table_id>`), not `dbfs:/user/hive/warehouse/`; (4) **Predictive Optimization** now runs `OPTIMIZE` / `VACUUM` / `ANALYZE` *automatically* on UC managed tables — the manual maintenance commands in §7–§8 are still valid but increasingly the platform's job, not yours. See [research-cache](../../research-cache/dcde-sg-ch02-facts.md).

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

## 2. How Data Is Stored in Delta Lake

A Delta table is **just a set of objects under one path prefix in a cloud storage bucket** (S3 / ADLS / GCS) — no proprietary database, no special storage engine. (Object storage has no real folders; the `/` in a key is just text, so the "directories" below are a convenient way to picture key prefixes.) Two kinds of objects share the prefix: **Parquet data files** (the rows) and the **`_delta_log/`** files (the transaction log that tracks which data files belong to the table). Understanding this layout explains everything else in the chapter — time travel, ACID, OPTIMIZE, VACUUM all operate on these files.

### 2.1 The table directory (anatomy)

```text
<table-storage-location>/                   ← the table = a directory in object storage
│                                             UC managed → under the catalog's storage root
│                                             legacy hive_metastore → dbfs:/user/hive/warehouse/…
├── part-00000-....snappy.parquet           ← data files (immutable Parquet)
├── part-00001-....snappy.parquet
├── part-00002-....snappy.parquet           ← written by a later UPDATE; old file kept until VACUUM
└── _delta_log/                             ← the transaction log
    ├── 00000000000000000000.json           ← one JSON per committed version
    ├── 00000000000000000001.json
    ├── 00000000000000000002.json
    ├── ...
    ├── 00000000000000000010.checkpoint.parquet   ← checkpoint every ~10 commits
    └── _last_checkpoint                     ← pointer to newest checkpoint
```

> **Partitioning vs. the flat layout above.** The tree shows an *unpartitioned* table. With `PARTITIONED BY (category)`, the `part-*.parquet` files instead sit under `category=Toys/`, `category=Kitchen/`, … subdirectories — a table is one or the other, never both. Liquid clustering (§7, the 2026 recommendation) uses no partition directories at all.
>
> Partitioning still works but is **discouraged for new tables**:
> 
> - Don't partition tables **< 1 TB**, and keep any partition **≥ 1 GB**. Since DBR 11.3 LTS unpartitioned tables already get **ingestion-time clustering** for free; use liquid clustering (§7) for everything else.
> - **Managed Iceberg** tables can't be Hive-partitioned at all — `PARTITION BY` is reinterpreted as liquid-clustering keys.
> - Convert an existing partitioned table: `ALTER TABLE … REPLACE PARTITIONED BY WITH CLUSTER BY` (DBR 18.1+).
> - The `col=value/` dirs are **not part of the Delta protocol** — Delta finds files via the transaction log + per-file stats, not paths. Workloads must never depend on the directory layout (with column mapping enabled, the dir names even become random prefixes).

Inspect it from a notebook:

```sql
DESCRIBE DETAIL product_info;   -- location, format=delta, numFiles, sizeInBytes
```
```python
# Raw-file listing works on legacy hive_metastore tables (DBFS root); blocked on UC managed tables.
%fs ls 'dbfs:/user/hive/warehouse/product_info'             # data files + _delta_log/
%fs ls 'dbfs:/user/hive/warehouse/product_info/_delta_log'  # the JSON + checkpoint files
```

> ⚠️ **About the `dbfs:/user/hive/warehouse/...` paths.** That location is the **DBFS root**, and DBFS root (along with DBFS mounts) is **deprecated** — new 2026 accounts are provisioned without it. The book's paths only work because it uses `hive_metastore`; they're shown here to expose the raw file layout. On a real UC workspace, **managed tables** live in UC-governed managed storage (`…/__unity_storage/catalogs/<catalog_id>/tables/<table_id>` — addressed by GUIDs, not a friendly path) where UC controls access via full cloud-URI grants, so you don't browse them with `%fs ls`; for ad-hoc files use **Unity Catalog volumes** / external locations instead. Note the `dbfs:/` *scheme* itself is not deprecated — it's still a valid optional prefix for UC volume paths; only DBFS **root** and **mounts** are.

> ⚠️ **`hive_metastore` is legacy too.** It still appears as a top-level catalog in the 3-level namespace (`hive_metastore.<schema>.<table>`) and UC runs *alongside* it, so the book's demos work. But the per-workspace Hive metastore is a **legacy feature**: its tables get no UC governance (audit, lineage, access control), the **Databricks-hosted** legacy Hive metastore has resource limits (concurrent connections + connections/hour, which can fail jobs), and Databricks recommends migrating tables to UC then **disabling** direct HMS access. Auto-enabled UC workspaces default to the *workspace* catalog, not `hive_metastore`. **Accounts created after 2025-12-19 have HMS (and DBFS root, no-isolation clusters, DBR < 13.3 LTS) disabled by default with no opt-out** — so a brand-new 2026 account is UC-only and the book's `hive_metastore` / `dbfs:` demos won't run until a workspace admin re-enables those legacy features. Treat the `hive_metastore` path tricks here as "older workspace / local-practice" only — new work goes in Unity Catalog.

### 2.2 Data files — Parquet

The rows live in **Parquet** files. Parquet is the storage *format*; Delta Lake is the *layer* that manages those files. Properties that matter here:

- **Columnar** — values are stored column-by-column, not row-by-row. A query reads only the columns it references (column pruning) and skips the rest; and because each column holds one type with similar values, per-column encoding + compression (snappy by default) reaches far higher ratios than a row format could.
- **Immutable** — a Parquet file is never edited in place. Every UPDATE / DELETE / MERGE writes *new* files and soft-deletes old ones in the log (see §3.2). This immutability is what makes time travel and ACID possible.
- **Splittable + self-describing** — a Parquet file is divided into **row groups** (horizontal blocks of rows, ~128 MB), and the file footer records each row group's byte offset, length, and stats. Spark reads the footer, then hands each row group to a separate task → parallel scan of a single file, with no external metadata service. (Contrast a gzipped CSV: its compression spans the whole stream, so it's *not* splittable — one task must read it end-to-end. Parquet compresses per-column-chunk *inside* each row group, so every split decompresses independently.)

Each `INSERT` (or any write) produces one or more new Parquet files — it never appends to an existing one. Many small writes → many small files, which is the problem `OPTIMIZE` solves (§7).

### 2.3 The transaction log (`_delta_log/`)

The log is the **source of truth** for what the table *is*. The Parquet files on disk are meaningless on their own — only files the log references are part of the table.

- Each committed transaction → **one JSON file** (`...0000.json`, `...0001.json`, …). The number is the table **version**.
- A JSON entry records: the operation (`commitInfo`: WRITE / UPDATE / DELETE / OPTIMIZE…), the predicate used, files **`add`**ed, and files **`remove`**d (soft-deleted, not erased from storage).
- Each `add` entry also carries **per-file statistics** — row count plus min/max and null counts for the leading columns. The engine reads these and **skips** any Parquet file whose min/max range can't match a query predicate (*data skipping*) without opening the file. This is exactly what `OPTIMIZE … ZORDER` / liquid clustering tune (§7).
- Optional `.crc` files (one per version, `{version}.crc` — the *Version Checksum*) record the table's state at that version so readers can validate integrity and detect non-compliant edits to the append-only log.

```python
%fs head 'dbfs:/.../product_info/_delta_log/00000000000000000003.json'
# {"commitInfo":{"operation":"UPDATE", ...}}
# {"remove":{"path":"part-...c000.snappy.parquet","deletionTimestamp":...}}
# {"add":   {"path":"part-...c000.snappy.parquet","stats":"{\"numRecords\":..,\"minValues\":..}"}}
```

### 2.4 Checkpoints

Replaying thousands of tiny JSON files would be slow. So **every 10 commits** Delta writes a **`.checkpoint.parquet`** that consolidates the full table state up to that version into one Parquet file, and updates `_last_checkpoint` to point at it. (Book doesn't cover this; exam occasionally mentions it.)

A checkpoint is **not a transaction** — it writes no new `.json` and does **not** increment the table version. It rides along *after* the commit that produced version N: `00...0N.json` (from the operation, e.g. an INSERT) and `00...0N.checkpoint.parquet` (the summary) share the same version N. Only real operations (INSERT, UPDATE, OPTIMIZE, RESTORE…) create JSON commits and bump the version; checkpointing is pure read-side bookkeeping.

**What happens to the JSON commits?** Writing a checkpoint does **not** delete them — the checkpoint is only a *read shortcut*. The JSON files stay so you can still `DESCRIBE HISTORY` and time-travel to versions before the checkpoint. They're removed later, **automatically and asynchronously after a checkpoint**, once older than `delta.logRetentionDuration` (default **30 days**). Two retention windows act independently:

| Property | Governs | Default |
|---|---|---|
| `delta.logRetentionDuration` | log files (JSON + checkpoints) → history/time-travel *metadata* | 30 days |
| `delta.deletedFileRetentionDuration` | obsolete Parquet *data* files → what `VACUUM` removes (§8) | 7 days |

Because VACUUM clears data files at 7 days but the log is kept 30, **actual time travel is usually bounded by VACUUM (7 days), not the log**. Time travel needs **both** the metadata (log/checkpoint says "version N = files X, Y, Z") *and* those data files still on storage. The checkpoint stores only file *references* + stats, never a copy of the rows — so once VACUUM deletes X/Y/Z, `SELECT … VERSION AS OF N` **fails** with a file-not-found error even though the checkpoint still knows about them. Surviving metadata ≠ surviving data. Also note Delta needs *all consecutive* JSON entries since the prior checkpoint — if early commits are cleaned, you can't time-travel to versions between them and that checkpoint.

**Why log retention ≥ data retention (and when to widen the gap).** The default split (30 vs 7) is deliberate, and **log must never be shorter than data** — DBR 18.0+ enforces `logRetentionDuration ≥ deletedFileRetentionDuration`. Reason: the log is the source of truth for which files are garbage, and `deletedFileRetentionDuration` is counted *from the commit that removed a file* — that timestamp lives in the log. Clean the log faster than the data and VACUUM loses the record of when files became obsolete → orphaned files / unreadable recent versions. Metadata must outlive the data it describes.

Tuning the two windows:

- **Keep log ≫ data** when you want a **cheap long audit trail** (who/what/when/predicate for 30–90 d) without paying to retain heavy data files, or to protect **lagging streaming / CDF consumers** that track the table by version (set `logRetentionDuration` ≥ worst-case consumer downtime, see §2.6).
- **Raise data toward log** only when you need longer *real* rollback (`RESTORE` / `VERSION AS OF`). For N-day time travel set **both** to N — and pay storage for all the obsolete files that now linger.
- Rules of thumb: long audit + modest recovery → leave defaults; N-day rollback → both = N; lagging streams → `logRetentionDuration` ≥ max lag.

### 2.5 How a read reconstructs the current state

1. Read `_last_checkpoint` → jump to the newest `.checkpoint.parquet`.
2. Replay the JSON commits *after* that checkpoint.
3. Net the `add` minus `remove` entries → the exact set of valid Parquet files for the current (or a time-travelled) version.
4. Use each file's min/max stats to skip files that can't match the query, then scan only the survivors.

This is also why Delta gives **ACID**: a write only "commits" when its JSON entry lands. An interrupted write may leave a stray Parquet file on storage, but with no log entry it's invisible to every reader (covered scenario-by-scenario in §3).

### 2.6 Streaming inserts: commits, checkpoints, and the real bottleneck

A streaming write commits **once per micro-batch, not per row**. Each trigger = one Delta transaction = **one JSON file = one version** — even if that micro-batch writes many Parquet data files. A 10-second trigger therefore produces ~8,640 JSON commits/day; high-frequency streaming *does* pile up log files fast.

Checkpoints follow the same `checkpointInterval` rule (default **10 commits**) — one `.checkpoint.parquet` every 10 micro-batches. (As in §2.4, the checkpoint is not itself a commit: no new version/JSON.)

**Why the log doesn't become the bottleneck:**

- **Checkpoints cap replay cost.** A reader never replays all 8,640 files — it jumps to the newest checkpoint and replays only the ≤10 JSON commits since. State reconstruction is **O(checkpointInterval), not O(total commits)**: the commit count grows, planning cost doesn't.
- **Log cleanup bounds the directory.** Old JSON + checkpoints are removed after `logRetentionDuration` (30 d), so `_delta_log/` doesn't grow without limit.
- **Single writer, no contention.** One streaming query owns the log; appends don't conflict, so commits serialize cleanly with no retry storms.

**The real bottleneck is small data files, not the log.** Each micro-batch writes small Parquet files → the *small-file problem*, which degrades reads. Mitigations:

- **Optimized writes** (`delta.autoOptimize.optimizeWrite`) + **auto-compaction** (`delta.autoOptimize.autoCompact`) — Delta compacts small files as the stream runs.
- **Predictive optimization** (UC managed tables) runs OPTIMIZE/VACUUM for you (§7–§8).
- **Tune the trigger** — larger / less frequent batches (e.g. `Trigger.AvailableNow`, longer processing-time) → fewer commits and fewer small files.

> 💡 Don't confuse the two "checkpoints": the **Delta log checkpoint** (`_delta_log/*.checkpoint.parquet`, a read shortcut for table state) is unrelated to the **Structured Streaming checkpoint** (a separate `_checkpoints/` dir holding stream *offsets* for exactly-once resume). VACUUM skips `_`-prefixed dirs, so the streaming checkpoint is safe.

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
