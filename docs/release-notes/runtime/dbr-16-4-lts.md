# Databricks Runtime 16.4 LTS Release Notes

> **Source:** [docs.databricks.com/aws/en/release-notes/runtime/16.4lts](https://docs.databricks.com/aws/en/release-notes/runtime/16.4lts)
> **GA date:** 2025-05-09
> **Added:** 2026-06-11

## Core versions

| Component | Version |
|---|---|
| Apache Spark | 3.5.2 |
| Python | 3.12.3 |
| Delta Lake | 3.3.1 |
| Scala | 2.12.15 or 2.13.10 |

---

## New features

**Auto Loader type widening (Public Preview)**
Automatically widens data types without data rewrite. New `addNewColumnsWithTypeWidening` mode handles `int → long`, `float → double`.

**Auto Loader `cloudFiles.cleanSource`**
Automatically manages (deletes) processed source files after ingestion.

**Streaming Delta type widening**
Type widening extends to Delta streaming reads and Delta Sharing scenarios.

**`listagg` and `string_agg`**
New aggregate functions for grouping STRING and BINARY values into delimited lists.

**`IDENTIFIER` clause for catalog operations**
Dynamic catalog naming in `CREATE`, `DROP`, `COMMENT ON`, `ALTER CATALOG`.

**Filter pushdown for Python data sources**
Reduces processing overhead for custom Python data source implementations.

**Dashboards, alerts, queries as workspace files (GA)**
Programmatic interaction with SQL assets as filesystem objects.

---

## Breaking changes

**Scala 2.12 → 2.13 migration (if using Scala 2.13 variant)**
Collection APIs differ. HashMap and Set ordering may differ — code relying on implicit ordering may break.

**Query plan caching with options**
File source table reads now respect query options (e.g., delimiters). Previously only initial plans were cached.

**Source materialization in MERGE**
Cannot be disabled — configuration flag enforcement.
