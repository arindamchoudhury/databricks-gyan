# Platform Release Notes — January 2026

> **Source:** [docs.databricks.com/aws/en/release-notes/product/2026/january](https://docs.databricks.com/aws/en/release-notes/product/2026/january)
> **Added:** 2026-06-11

---

## Data Engineering highlights

### Lakeflow Connect

**Row filtering for managed connectors (Beta)**
Conditional data selection for Google Analytics, Salesforce, and ServiceNow sources — reduce ingestion volume with WHERE-like conditions.

**Google Drive connector (Beta)**
File ingestion from Google Drive using `read_files`, `spark.read`, `COPY INTO`, and Auto Loader.

**Salesforce formula fields incremental ingestion (Beta)**
Optional incremental processing for Salesforce formula fields — improves performance vs snapshot.

### Lakeflow Jobs

**System tables (GA)**
Four new system tables now generally available:
- `system.lakeflow.jobs`
- `system.lakeflow.job_tasks`
- `system.lakeflow.job_run_timeline`
- `system.lakeflow.job_task_run_timeline`

Query account-wide job and run insights via SQL.
> **Learning path note (A6):** These system tables are the foundation of the observability dashboard exercise in A6.

**Trigger-on-update for pipelines (GA)**
Auto-refresh pipelines when a source table changes — use in Databricks SQL when creating a pipeline schedule.

### Serverless / Compute

**Custom base environments for serverless jobs**
YAML-defined custom environments for Python, wheels, and notebook tasks.

**DBR 18.0 (GA)** — Apache Spark 4.1.0.

**Lakebase (GA)**
Autoscaling, scale-to-zero, instant branching, automated backups, PITR, storage up to 8 TB.

**Serverless workspaces (GA)**
Pre-configured workspace with serverless compute and default storage — no infra setup needed.
