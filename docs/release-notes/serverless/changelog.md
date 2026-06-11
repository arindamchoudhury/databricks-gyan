# Serverless Compute — Release Notes

> **Source:** [docs.databricks.com/aws/en/release-notes/serverless/](https://docs.databricks.com/aws/en/release-notes/serverless/)
> **Added:** 2026-06-11

Serverless versions track closely to Databricks Runtime versions. Key versions for data engineering:

---

## Serverless 18.2 (May 13, 2026)

Based on DBR 18.2 / Spark 4.1.0.

**New:**
- `CREATE OR REPLACE TEMP TABLE` syntax
- `agg()` alias for `measure()`
- Delta table history includes write option flags
- `df.replaceOn` and `df.replaceUsing` APIs (GA) — selective data replacement

**Breaking/Behavior:**
- NULL struct preservation in INSERT, MERGE, streaming with schema evolution
- `LEFT OUTER JOIN LATERAL` row-drop bug fixed
- `NATURAL JOIN` respects case-insensitive matching
- SQL UDF dependency validation enforced
- AWS SDK v1 shaded

---

## Serverless 18.1 (April 20, 2026)

**New:**
- `WITH SCHEMA EVOLUTION` for INSERT statements
- Delta Sharing multi-statement transaction support
- `parse_timestamp` with Photon support
- `max_by` / `min_by` with optional limit (up to 100,000)
- Vector functions: `vector_avg`, `vector_sum`, `vector_cosine_similarity`, `vector_inner_product`, `vector_l2_distance`, `vector_norm`, `vector_normalize`
- SQL cursor support (DECLARE CURSOR, OPEN, FETCH, CLOSE)
- Approximate top-k and tuple sketch functions
- New geospatial functions

---

## Serverless 18.0 (February 27, 2026)

**New:**
- SQL scripting GA
- SQL window functions in metric views
- Dynamic shuffle partition adjustment in stateless streaming queries
- AQE and auto-optimized shuffle support
- Literal string coalescing everywhere
- Parameter markers virtually anywhere
- `IDENTIFIER` clause expanded
- `BITMAP_AND_AGG` aggregate
- Theta sketch function library
- KLL sketch function library
- New geospatial functions

**Breaking/Behavior:**
- `FSCK REPAIR TABLE` includes metadata repair by default
- Python UDF execution unified; TIMESTAMP no longer includes timezone
- Time travel hard-blocked beyond `deletedFileRetentionDuration`
- Partition columns materialized in Parquet files
- `BinaryType` → `bytes` by default in PySpark

---

## Serverless Environment Version 5 (February 25, 2026)

New environment for both CPU and GPU serverless notebooks and jobs.

**`%uv pip`** — faster package installs (env version 5+).

---

## Serverless 17.3 (October 28, 2025)

- `LIMIT ALL` for recursive CTEs
- `st_dump`, `st_numinteriorrings`, `st_interiorringn` geospatial functions
- `EXECUTE IMMEDIATE` with constant expressions
- `spark.sql.files.maxPartitionBytes` now configurable

---

## Serverless Performance Mode (GA) (June 10, 2025)

Performance-optimized setting for jobs and pipelines GA.
- **Performance mode** — faster startup and execution (higher DBU cost)
- **Standard mode** — optimizes for cost (slightly higher launch latency)

Not supported for: continuous pipelines, one-time runs, SQL warehouse tasks.

---

## Serverless 16.4 (May 28, 2025)

- Auto Loader `cloudFiles.cleanSource`
- Type widening for streaming Delta reads
- `listagg` / `string_agg` aggregate functions
- Filter pushdown for Python data sources

---

## Serverless 16.1 (February 5, 2025)

- **`OPTIMIZE FULL`** — forces full reclustering (vs incremental `OPTIMIZE`)
- `VACUUM LITE` mode (Public Preview)
- Liquid clustering during streaming writes via `clusterBy`
- Identity columns in Delta Python APIs
- `withSchemaEvolution()` for DeltaMergeBuilder
- New SQL functions: `try_url_decode`, `zeroifnull`, `nullifzero`, `dayname`, `uniform`, `randstr`

> **Learning path note (A2):** `OPTIMIZE FULL` is the escape hatch when incremental clustering hasn't converged — force a full re-layout.

---

## Serverless 15.4 (October 28, 2024)

- Enable UniForm Iceberg via `ALTER TABLE` without data rewriting
- `COPY INTO` query latency improvement
- UTF-8 validation functions: `is_valid_utf8`, `make_valid_utf8`, `validate_utf8`, `try_validate_utf8`

---

## Serverless 14.3 (April 15, 2024)

First serverless version. Key deprecations vs classic compute:
- `input_file_name()`, `input_file_block_length()`, `input_file_block_start()` deprecated — use `_metadata` column
- Most manual Spark configs removed — check serverless-supported config list
