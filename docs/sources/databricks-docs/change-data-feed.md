# Change data feed (CDF)

> **Source:** [docs.databricks.com/aws/en/tables/features/change-data-feed](https://docs.databricks.com/aws/en/tables/features/change-data-feed)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** tables, delta, iceberg, change-data-feed, cdf, table_changes, readChangeFeed, row-tracking, structured-streaming, incremental-etl, cdc, gdpr, I5, I4, A4
> **Type:** documentation

CDF tracks **row-level changes between versions** of a Delta Lake (or Apache Iceberg v3) table. There are two implementations that expose the **same `table_changes()` / `readChangeFeed` APIs** — so reader code is identical and the choice is a write-side performance/cost vs availability tradeoff. It's used for **incremental ETL** (process only changed rows), **audit trails** (compliance), and **data replication / delete propagation** (sync changes downstream). Metadata columns are `_change_type` (insert / update_preimage / update_postimage / delete), `_commit_version`, `_commit_timestamp` — a column-name collision with these blocks CDF until renamed.

## Automatic vs Legacy

| | Automatic CDF (Public Preview) | Legacy CDF |
|---|---|---|
| When computed | Read / query time | Write time (materialized) |
| Config | None per-table (uses row tracking / row lineage) | `delta.enableChangeDataFeed=true` per table |
| Formats | Delta Lake **+ Apache Iceberg v3** | Delta Lake only |
| Min runtime | DBR 18+ | (long-standing) |
| Write cost | Lower — MERGE/UPDATE don't write change files | Higher — change files on write |
| APIs | `table_changes()`, `readChangeFeed` | same |

> "Because changes are not computed on every write for MERGE INTO and UPDATE operations, automatic change data feed improves write performance and reduces storage costs, compared to legacy change data feed."

**You can't run both** on the same table; Databricks recommends migrating to automatic. Automatic CDF works with batch, Structured Streaming, and D2D Delta Sharing, and is one of the features [[automatic-upgrades]] can auto-enable (needs row tracking on). Only **Databricks readers** can query CDF — it's not in the Iceberg spec, so external Iceberg readers can't.

## Requirements (Automatic CDF)

- **DBR 18+**.
- UC-registered supported format: **managed** Delta w/ row tracking enabled **or** Iceberg v3; **external** Delta w/ row tracking enabled.

## Reading CDF

**Batch** — a starting version is **required** (integer version or `yyyy-MM-dd[ HH:mm:ss[.SSS]]` timestamp); start+end inclusive; a version before CDF was enabled errors.

```python
spark.read.option("readChangeFeed", "true").option("startingVersion", 0).table("<table_name>")
```

```sql
SELECT * FROM table_changes('tableName', 0, 10);                                          -- version range
SELECT * FROM table_changes('tableName', '2021-04-21 05:45:46', '2021-05-21 12:00:00');   -- timestamp range
SELECT * FROM table_changes('tableName', 0);                                              -- from version to latest
```

**Streaming** — required for Databricks to auto-track versions. On first start, returns the **latest snapshot as INSERT records**, then future changes.

```python
spark.readStream.option("readChangeFeed", "true").table("myTable")
```

Rate limits (`maxFilesPerTrigger`, `maxBytesPerTrigger`, `excludeRegex`) apply **atomically per commit** for non-snapshot versions (a batch takes a whole commit or defers it). For SCD type 1/2 CDC, use the AUTO CDC pipeline APIs instead (I4).

## Specify a starting version

Required for batch reads; optional ending version. For streaming, the default (record all existing rows as INSERT) suits new pipelines; specify a starting version if the target already has rows up to a point. **Recovery from a corrupted checkpoint:** define the stream with `startingVersion` = (last-processed + 1) and a **new** checkpoint location.

```python
(spark.readStream.option("readChangeFeed", "true").option("startingVersion", 76).table("source_table")
  .writeStream.option("checkpointLocation", "<new-checkpoint-path>").toTable("target_table"))
```

> ⚠️ If the starting version isn't in table history, the stream fails to start from a new checkpoint. **Managed tables auto-clean historic versions**, so all starting versions are eventually deleted.

## Out-of-range versions

A version/timestamp past the last commit errors with `timestampGreaterThanLatestCommit`. DBR 11.3 LTS+ tolerance: `SET spark.databricks.delta.changeDataFeed.timestampOutOfRange.enabled = true;` — then starting beyond last commit → empty result; ending beyond → all changes from start to last commit.

## Archive for permanent history

> "A change data feed is not intended to serve as a permanent record of all changes to a table. It only records changes that occur after change data feed was enabled."

CDF records are transient (purged with the table's version retention). To keep a permanent change log, incrementally write CDF records to a new table:

```python
(spark.readStream.option("readChangeFeed", "true").table("source_table")
  .writeStream.option("checkpointLocation", "<checkpoint-path>").trigger(availableNow=True).toTable("target_table"))
```

## Legacy CDF specifics

```sql
CREATE TABLE student (id INT, name STRING, age INT) TBLPROPERTIES (delta.enableChangeDataFeed = true);   -- new
ALTER TABLE myDeltaTable SET TBLPROPERTIES (delta.enableChangeDataFeed = true);                          -- existing
ALTER TABLE <table_name> UNSET TBLPROPERTIES ('delta.enableChangeDataFeed');                             -- migrate to automatic
```

> If legacy CDF is turned off for an interval then back on, that interval is **not queryable** (use automatic CDF to query it).

Storage: a small bump (changes in separate files); insert-only and full-partition deletes generate **no** change files (computed from the transaction log); change files follow VACUUM retention. Never reconstruct CDF by reading change files directly — always use the APIs.

## Limitations

- **Column mapping:** after non-additive schema changes (rename/drop column, type change, nullability) you **can't read CDF across** that transaction. Batch reads use the range's end-version schema but still fail if the range spans a non-additive change (split into ranges).
- **Automatic CDF only:** external Iceberg clients can't query it; not supported if the source was modified during a **multi-statement transaction**; **not supported on tables with row filters or column masks**.

Related: [[automatic-upgrades]], [[managed-tables]], [[external-tables]], [[liquid-clustering]], [[predictive-optimization]], [[tables-concepts]].
