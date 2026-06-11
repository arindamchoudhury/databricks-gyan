# Databricks Runtime 17.3 LTS Release Notes

> **Source:** [docs.databricks.com/aws/en/release-notes/runtime/17.3lts](https://docs.databricks.com/aws/en/release-notes/runtime/17.3lts)
> **GA date:** 2025-10-22
> **Added:** 2026-06-11

## Core versions

| Component | Version |
|---|---|
| Apache Spark | 4.0.0 |
| Python | 3.12.3 |
| Delta Lake | 4.0.0 |
| Java | Zulu17.58+21-CA (JDK 17) |
| Scala | 2.13.16 |
| OS | Ubuntu 24.04.3 LTS |

---

## Breaking changes

**`input_file_name()` removed**
The function is no longer supported — it was unreliable. Use `_metadata.file_name` instead.
> ⚠️ **Learning path note (I1):** Auto Loader pipelines or ingestion code using `input_file_name()` will break on DBR 17.3+. Replace with `df.select("_metadata.file_name")`.

**Auto Loader default changed**
`cloudFiles.useIncrementalListing` now defaults to `false` (was `auto`). Full directory listings are now the default to prevent skipped files due to non-lexicographic file ordering.

---

## New features

**Fine-grained access control for append (GA)**
Append data to UC tables using fine-grained access control on dedicated compute.

**`EXECUTE IMMEDIATE` with constant expressions**
Enables dynamic SQL execution with constant-expression parameters.

**Recursive CTEs with `LIMIT ALL`**
Overrides size restrictions on recursive common table expressions.

**Python UDTFs with TABLE arguments**
UC Python UDTFs can now accept TABLE arguments for complex multi-row input transformations.

**Geospatial:** `st_dump`, `st_numinteriorrings`, `st_interiorringn` functions added.

**`remote_query` TVF (Public Preview)**
Queries remote databases using UC credentials — useful for federated access.

---

## Fixes

- Temporal value conversion in struct literals
- Null handling in Parquet files
- Case class conversion in array/map literals in Spark Connect mode
