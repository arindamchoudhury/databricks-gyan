# Databricks Runtime 18 Release Notes

> **Source:** [docs.databricks.com/aws/en/release-notes/runtime/18](https://docs.databricks.com/aws/en/release-notes/runtime/18)
> **GA date:** 2026-06-10
> **Added:** 2026-06-11

## Core versions

| Component | Version |
|---|---|
| Apache Spark | 4.1.0 |
| Python | 3.12.3 |
| Delta Lake | 4.2.0 |
| Java | Zulu21.42+19-CA (JDK **21**) |
| Scala | 2.13.16 |
| OS | Ubuntu 24.04.4 LTS |
| PyArrow | 21.0.0 |
| pandas | 2.2.3 |

---

## Breaking changes

> ⚠️ **Review these before migrating production workloads to DBR 18.**

**JDK 17 → JDK 21**
Floating-point string representations differ between JDK versions. Code that parses or compares float-to-string output may break.

**Arrow becomes default interchange for Python UDFs**
Previously opt-in; now default. Timezone metadata **dropped** from TIMESTAMP inputs to Python UDFs.
> **Learning path note (B3/A1):** Python UDFs receiving TIMESTAMP columns will no longer see timezone info. Adjust UDFs that relied on timezone-aware timestamps.

**NULL struct handling changed**
NULL structs now preserved as NULL (not materialized as non-null structs with all-NULL fields) in MERGE, INSERT, and streaming with schema evolution.
> **Learning path note (I5):** If you write MERGE statements that relied on the old NULL struct behavior, test carefully.

**NATURAL JOIN case sensitivity**
Now respects `spark.sql.caseSensitive` configuration.

**AWS SDK v1 shaded**
No longer available on classpath for user code.

**Partition column materialization**
Partition values written to Parquet files — affects direct file readers that expect partition columns only in directory paths.

**Time travel blocked beyond `deletedFileRetentionDuration`**
Previously allowed with a warning; now raises an error.
> **Learning path note (I5):** VACUUM + time travel interaction — if you VACUUM aggressively (< 7 days), time travel will now hard-fail instead of warn.

---

## New features

### SQL & Query Processing

- **SQL scripting (GA)** — procedural logic inside SQL
- **IP address functions (Public Preview)** — IPv4/IPv6 operations
- **NEAREST BY join type** — top-K nearest-neighbor queries
- **QUALIFY clause** — filter on window function results directly
- **Parameter markers** (`:param`, `?`) — work virtually anywhere a literal is permitted

### Streaming

- **On-demand state repartitioning (Public Preview)** — for stateful streaming queries
- **Structured Streaming deduplication** — NaN values now handled correctly
- **Stream-stream non-outer joins** — support Update mode output

### Data Management

- **Auto CDC from snapshot** — SQL syntax now available
- **Schema evolution with INSERT** — `WITH SCHEMA EVOLUTION` clause
- **Partition column materialization** — partition values written to Parquet data files

### Analytics

- **Vector aggregate functions:** `vector_avg`, `vector_sum`, `vector_norm`, `vector_normalize`
- **Theta sketch and KLL sketch functions** for approximate computation
- **`array_sort` with custom comparators** now accelerated by Photon
- **`max_by` / `min_by`** accept optional `limit` parameter

---

## Library upgrades

100+ package version updates. Highlights:

| Library | Version |
|---|---|
| PyArrow | 21.0.0 |
| pandas | 2.2.3 |
| R | 4.5.1 |
