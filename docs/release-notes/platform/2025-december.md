# Platform Release Notes — December 2025

> **Source:** [docs.databricks.com/aws/en/release-notes/product/2025/december](https://docs.databricks.com/aws/en/release-notes/product/2025/december)
> **Added:** 2026-06-11

---

## Data Engineering highlights

### Lakeflow Pipelines

**ForEachBatch for declarative pipelines (Public Preview)**
Process streams as micro-batches in Python — new capability for custom per-batch logic inside Lakeflow pipelines.

### Auto Loader

**File events (GA)**
Auto Loader can now discover files with the efficiency of notifications while retaining the simplicity of directory listing. No need to choose between the two modes.

### Lakeflow Connect — new connectors

| Connector | Status |
|---|---|
| MySQL | Public Preview — incremental ingestion from MySQL and Amazon RDS |
| PostgreSQL | Public Preview |
| Meta Ads | Beta |
| Confluence | Beta — spaces, pages, attachments, metadata |
| Jira | Beta — issues, comments, attachment metadata |
| NetSuite | Public Preview |
| Microsoft Dynamics 365 | Public Preview — Sales, Customer Service, Finance & Operations |
| SharePoint (custom) | Beta |

### Governance — Important deprecation

> **⚠️ Breaking for new accounts:** New Databricks accounts created after December 18, 2025 have **no access** to:
> - DBFS root and mounts
> - Hive Metastore
> - No-isolation shared compute
>
> **Learning path note (B1, I7):** The learning path already recommends UC over Hive Metastore. If starting fresh, you will not encounter Hive Metastore at all.

**Context-based ingress control (Public Preview)**
Admins set allow/deny rules combining who + from where + what they can reach.

### SQL / Materialized Views

**Materialized view and streaming table ownership**
Users can now modify ownership of MVs and streaming tables in Catalog Explorer.

**Lakebase Autoscaling (Public Preview)**
Autoscaling compute, scale-to-zero, branching, instant restore. SQL editor read-write access + ACL permissions.

### Runtime

**DBR 18.0 (Beta)** — Apache Spark 4.1.0, JDK 21 default.

**Excel file support (Beta)**
Query Excel files directly via Spark DataFrames without external libraries.
