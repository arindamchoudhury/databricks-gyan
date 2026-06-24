# Change data feed (CDF)

> **Source:** [docs.databricks.com/aws/en/tables/features/change-data-feed](https://docs.databricks.com/aws/en/tables/features/change-data-feed)
> **Added:** 2026-06-24
> **Source updated:** 2026-06-11
> **Tags:** tables, delta, iceberg, change-data-feed, cdf, table_changes, readChangeFeed, row-tracking, structured-streaming, incremental-etl, cdc, gdpr, I5, I4, A4
> **Type:** documentation

## Summary

CDF tracks **row-level changes between versions** of a Delta Lake (or Apache Iceberg v3) table. Two implementations: **Automatic CDF** (Public Preview) computes changes *at read time* from row-lineage metadata — no per-table config, works on Delta + Iceberg v3, DBR 18+; **Legacy CDF** materializes changes *at write time* — Delta-only, per-table `delta.enableChangeDataFeed`. **Both expose the same `table_changes()` / `readChangeFeed` APIs**, so reader code is identical; the choice is a write-side performance/cost vs availability tradeoff. Used for incremental ETL, audit trails, and replication/delete-propagation.

> Breadcrumb: Tables › Table functionality › Table features › Change data feed. The feature deep-dive behind the conceptual CDF coverage in I5 (enable + query) and A4 (GDPR delete propagation).

## Key points

- **Three use cases**: incremental ETL (process only changed rows), audit trails (compliance), data replication (sync changes downstream).
- **Automatic CDF (PP)**: changes computed **at query time** via row tracking (Delta) / row lineage (Iceberg v3). No per-table config. **Better write perf + lower storage** than legacy (MERGE/UPDATE don't materialize change files). Requires **DBR 18+**, UC-registered table (managed Delta w/ row tracking or Iceberg v3; external Delta w/ row tracking).
- **Legacy CDF**: change events **materialized on write**, Delta-only, turned on per-table with `delta.enableChangeDataFeed=true`. Databricks recommends migrating to automatic.
- **You can't run both** on the same table.
- **Only Databricks readers** can query CDF (Delta or Iceberg-v3-auto) — CDF is **not in the Iceberg spec**, so external Iceberg readers can't.
- **Metadata columns**: `_change_type` (insert / update_preimage / update_postimage / delete), `_commit_version`, `_commit_timestamp`. Column-name collision with these → can't use CDF until renamed.
- **Not a permanent log** — only records changes after CDF enabled; records are transient, purged with the table's version retention (VACUUM / checkpoint retention). Archive to a new table for permanent history.
- **Non-additive schema changes** (rename/drop column, type change, nullability) break CDF queries that span them.

## Notes

### Automatic vs Legacy

| | Automatic CDF (PP) | Legacy CDF |
|---|---|---|
| When computed | Read / query time | Write time (materialized) |
| Config | None per-table (uses row tracking / row lineage) | `delta.enableChangeDataFeed=true` per table |
| Formats | Delta Lake **+ Apache Iceberg v3** | Delta Lake only |
| Min runtime | DBR 18+ | (long-standing) |
| Write cost | Lower — MERGE/UPDATE don't write change files | Higher — change files on write |
| APIs | `table_changes()`, `readChangeFeed` | same |

Automatic CDF works with batch, Structured Streaming, and **D2D Delta Sharing**. It's also one of the features [[automatic-upgrades]] can auto-enable (PP, min DBR 18, needs row tracking on).

### Requirements (Automatic CDF)

- **DBR 18+**.
- UC-registered supported format: **managed** Delta w/ row tracking enabled **or** Iceberg v3; **external** Delta w/ row tracking enabled.
- CDF not in Iceberg spec → external Iceberg readers can't query it; for Delta, only Databricks readers can query CDF.

### Reading CDF

**Batch** — starting version **required** (integer version or `yyyy-MM-dd[ HH:mm:ss[.SSS]]` timestamp); start+end inclusive; a version before CDF was enabled errors.

```python
spark.read \
  .option("readChangeFeed", "true") \
  .option("startingVersion", 0) \
  .table("<table_name>")
```

```sql
SELECT * FROM table_changes('tableName', 0, 10);                                  -- version range
SELECT * FROM table_changes('tableName', '2021-04-21 05:45:46', '2021-05-21 12:00:00');  -- timestamp range
SELECT * FROM table_changes('tableName', 0);                                       -- from version to latest
SELECT * FROM table_changes('`schema`.`dotted.tableName`', '2021-04-21 06:45:46', '2021-05-21 12:00:00');  -- special chars
```

**Streaming** — required for Databricks to auto-track versions. On first start, returns the **latest snapshot as INSERT records**, then future changes.

```python
(spark.readStream
  .option("readChangeFeed", "true")
  .table("myTable"))
```

- Rate limits: `maxFilesPerTrigger`, `maxBytesPerTrigger`, `excludeRegex`. For non-snapshot versions, rate limits apply **atomically per commit** (a batch takes a whole commit or defers it).
- For SCD type 1/2 CDC processing, use the AUTO CDC APIs (pipelines) instead — see [[predictive-optimization]] sibling features / I4.

### Specify a starting version

- Required for batch reads; optional ending version.
- Streaming: default (record all existing rows as INSERT) suits new pipelines; specify a starting version if the target already has rows up to a point, to skip reprocessing as INSERTs.
- **Recovery from corrupted checkpoint**: define the stream with `startingVersion` = (last-processed + 1) and a **new** checkpoint location.

```python
(spark.readStream
  .option("readChangeFeed", "true")
  .option("startingVersion", 76)
  .table("source_table")
  .writeStream
  .option("checkpointLocation", "<new-checkpoint-path>")
  .toTable("target_table"))
```

> ⚠️ If the specified starting version isn't in table history, the stream fails to start from a new checkpoint. **Managed tables auto-clean historic versions**, so all starting versions are eventually deleted.

### Out-of-range versions

Default: a version/timestamp past the last commit → error `timestampGreaterThanLatestCommit`. DBR 11.3 LTS+ tolerance:

```sql
SET spark.databricks.delta.changeDataFeed.timestampOutOfRange.enabled = true;
```

- Starting beyond last commit → empty result.
- Ending beyond last commit → all changes from start to last commit.

### Archive for permanent history

CDF is transient. To keep a permanent change log, incrementally write CDF records to a new table (e.g. `trigger.AvailableNow` batch):

```python
(spark.readStream
  .option("readChangeFeed", "true")
  .table("source_table")
  .writeStream
  .option("checkpointLocation", "<checkpoint-path>")
  .trigger(availableNow=True)
  .toTable("target_table"))
```

### Legacy CDF specifics

```sql
-- new table
CREATE TABLE student (id INT, name STRING, age INT)
  TBLPROPERTIES (delta.enableChangeDataFeed = true);
-- existing table
ALTER TABLE myDeltaTable SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
-- migrate to automatic: turn legacy off first
ALTER TABLE <table_name> UNSET TBLPROPERTIES ('delta.enableChangeDataFeed');
```

> If legacy CDF is turned off for an interval then back on, that interval is **not queryable** (use automatic CDF to query it).

**Storage (legacy):** small storage bump (changes in separate files); insert-only and full-partition deletes generate **no** change files (computed from the transaction log); change files follow VACUUM retention. Never reconstruct CDF by reading change files directly — always use the APIs.

### Limitations

- **Column mapping**: after non-additive schema changes (rename/drop column, type change, nullability) you **can't read CDF across** that transaction/range. Batch reads use the range's **end-version schema**, but still fail if the range spans a non-additive change.
- **Automatic CDF only**: external Iceberg clients can't query it; not supported if the source table was modified during a **multi-statement transaction**; **not supported on tables with row filters or column masks**; queries can't span a non-additive schema change (split into ranges).

## Quotes worth keeping

> "Because changes are not computed on every write for MERGE INTO and UPDATE operations, automatic change data feed improves write performance and reduces storage costs, compared to legacy change data feed." (Automatic change data feed)

> "A change data feed is not intended to serve as a permanent record of all changes to a table. It only records changes that occur after change data feed was enabled." (Replay table history)

## Open questions

- Automatic CDF needs **row tracking** — and automatic-upgrades enables row tracking + auto-CDF together. Interaction with manually-enabled legacy CDF on the same table beyond "can't use both" not detailed here.

## Related sources

- [[automatic-upgrades]] — automatic CDF is one of the six features auto-upgrades can turn on (PP, DBR 18, requires row tracking).
- [[managed-tables]] / [[external-tables]] — CDF requirements differ by table type (managed Delta+row-tracking / Iceberg v3 vs external Delta+row-tracking).
- [[liquid-clustering]] / [[predictive-optimization]] — sibling Delta table features under Table functionality.
- [[tables-concepts]] — Delta vs Iceberg formats; CDF availability hinges on format + row tracking.
