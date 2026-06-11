# Platform Release Notes — March 2026

> **Source:** [docs.databricks.com/aws/en/release-notes/product/2026/march](https://docs.databricks.com/aws/en/release-notes/product/2026/march)
> **Added:** 2026-06-11

---

## Data Engineering highlights

### Delta Lake

**Type widening (GA)**
Column data types can now be widened (e.g., INT→BIGINT) without rewriting data files during ingestion.

**Auto Loader type widening (Public Preview)** — DBR 16.4+
Automatic type widening with new `addNewColumnsWithTypeWidening` mode: `int → long`, `float → double` across JSON, CSV, XML, Avro, Parquet.

**Multi-table transactions (Public Preview)**
`BEGIN ATOMIC ... END;` groups statements across multiple tables with automatic rollback on failure. Requires catalog commits on UC managed tables.

**Lineage system table enhancement**
`system.access.table_lineage` and `system.access.column_lineage` now include `genie_space_id` and `alert_id` fields.

### Databricks Asset Bundles → renamed

> **⚠️ Branding rename:** "Databricks Asset Bundles" is now called **"Declarative Automation Bundles"** (same functionality, renamed branding). CLI commands (`databricks bundle`) are unchanged.
> **Learning path note (A5):** The topic still uses "DABs" as abbreviation. Note the official name is now "Declarative Automation Bundles."

### Lakeflow Connect

**Workday HCM Connector (Beta)**
New managed connector for ingesting human capital data.

**Lakebase Change Data Feed (Beta)**
Continuously replicate Lakebase Postgres tables to UC Delta tables via CDC.

### Runtime

**DBR 18.1 (GA)**

### Workflows / Jobs

**SQL Alert Tasks (Beta)**
Execute Databricks SQL alert evaluations within job workflows.

**SQL pipeline notifications & performance mode (Beta)**
Materialized views and streaming tables support failure notifications and serverless performance configuration.

### Observability

**Data Quality Alerts UI (Beta)**
Create anomaly detection alerts from within the Data Quality Monitoring interface.

**Health indicators (Public Preview)**
Table freshness and completeness summaries in Catalog Explorer.
