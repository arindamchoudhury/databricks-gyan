# Databricks Release Notes

Captured from [docs.databricks.com/aws/en/release-notes/](https://docs.databricks.com/aws/en/release-notes/).
Last full refresh: **2026-06-11**.

> Run `/databricks-release-notes` to fetch the latest and update this section.

---

## Platform (monthly)

| Month | File | DE highlights |
|---|---|---|
| June 2026 | [2026-june](platform/2026-june/) | OpenSharing (Delta Sharing rebrand), external lineage GA, `@dp.update_flow` GA, new connectors |
| May 2026 | [2026-may](platform/2026-may/) | DBR 18 Beta, Lakeflow Designer default-on, Real-Time Mode, Sinks GA, Iceberg GA, DABs CLI GA |
| April 2026 | [2026-april](platform/2026-april/) | ABAC GA (breaking change), task disable GA, cascade delete Beta, pipeline retention extended |
| March 2026 | [2026-march](platform/2026-march/) | Type widening GA, Multi-table transactions Preview, DABs renamed to "Declarative Automation Bundles" |
| February 2026 | [2026-february](platform/2026-february/) | Pipeline dataset governance GA, file events default, SQL warehouse defaults GA |
| January 2026 | [2026-january](platform/2026-january/) | Lakeflow Jobs system tables GA, trigger-on-update GA, DBR 18.0 GA, Lakebase GA |
| December 2025 | [2025-december](platform/2025-december/) | ForEachBatch for pipelines Preview, MySQL/Postgres connectors, Auto Loader file events GA, legacy features removed for new accounts |

---

## Runtime

| Version | File | Spark | Python | Delta | Notes |
|---|---|---|---|---|---|
| DBR 18 | [dbr-18](runtime/dbr-18/) | 4.1.0 | 3.12.3 | 4.2.0 | JDK 21, Arrow default for UDFs (breaking), SQL scripting GA |
| DBR 17.3 LTS | [dbr-17-3-lts](runtime/dbr-17-3-lts/) | 4.0.0 | 3.12.3 | 4.0.0 | `input_file_name()` removed — use `_metadata.file_name` |
| DBR 16.4 LTS | [dbr-16-4-lts](runtime/dbr-16-4-lts/) | 3.5.2 | 3.12.3 | 3.3.1 | Auto Loader type widening, `listagg`, filter pushdown |

---

## Feature-specific

| Feature | File | Coverage |
|---|---|---|
| Lakeflow Spark Declarative Pipelines | [lakeflow/2026](lakeflow/2026/) | Jan–Apr 2026 monthly notes |
| Databricks SQL | [sql/2026](sql/2026/) | Jan–Jun 2026; SQL scripting GA, sketches, vector functions |
| Declarative Automation Bundles (DABs) | [dabs/changelog](dabs/changelog/) | 2024–2026; Python GA, direct deploy, selective deploy |
| Serverless Compute | [serverless/changelog](serverless/changelog/) | v14.3–18.2; all version notes |

---

## Learning path cross-references

Issues found while reviewing these notes that affect the learning path:

| Topic | Issue | Detail |
|---|---|---|
| A5 (DABs) | **Branding rename** | "Databricks Asset Bundles" is now branded "Declarative Automation Bundles" (March 2026). CLI commands (`databricks bundle`) unchanged. |
| A7 (Delta Sharing) | **Product rename** | "Delta Sharing" is now **OpenSharing** (June 2026). Same open protocol; new name. |
| B2/B3 | **Breaking: DBR 18 JDK 21** | JDK 17→21 changes floating-point string representations. |
| B3/A1 | **Breaking: Arrow default for Python UDFs** | DBR 18: Arrow is now the default interchange format for Python UDFs; timezone metadata dropped from TIMESTAMP inputs. |
| I1 (Auto Loader) | **Breaking: DBR 17.3** | `input_file_name()` removed. Use `_metadata.file_name` column instead. |
| I5 (Delta advanced) | **Breaking: DBR 18 NULL struct** | NULL structs now preserved as NULL (not materialized with all-NULL fields) in MERGE/INSERT/streaming. |
| I5 | **Breaking: DBR 18 time travel** | Time travel queries blocked beyond `deletedFileRetentionDuration`. Previously could go further back. |
| I5 | **New: `OPTIMIZE FULL`** | Serverless 16.1+: `OPTIMIZE FULL` forces full reclustering (vs incremental). |
