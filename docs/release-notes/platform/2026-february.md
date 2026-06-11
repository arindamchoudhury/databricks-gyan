# Platform Release Notes — February 2026

> **Source:** [docs.databricks.com/aws/en/release-notes/product/2026/february](https://docs.databricks.com/aws/en/release-notes/product/2026/february)
> **Added:** 2026-06-11

---

## Data Engineering highlights

### Lakeflow Pipelines

**Pipeline dataset governance (GA)**
Apply filters, masks, tags, and comments directly to ETL and ingestion pipeline outputs using `CREATE` and `ALTER` statements. Enables fine-grained governance at pipeline creation time.

**New managed connectors (Beta)**
TikTok Ads, HubSpot, Google Ads, Zendesk Support.

**Workspace admin pip config for pipelines**
Admins can configure private or authenticated package repositories as the default pip configuration for pipelines.

### Auto Loader

**File events now enabled by default**
When you create new external locations, file events are enabled automatically — no manual cloud resource configuration needed.

### SQL Warehouses

**Default warehouse settings (GA)**
Workspace and user-level default warehouse configuration now generally available.

**Query tagging (Public Preview)**
`SET QUERY_TAGS` and connector-level tagging for cost attribution and workload filtering.

**Activity details visualization (Beta)**
Shows query activity, fetching status, and idle periods on warehouse monitoring charts.

### Runtime

Maintenance updates for DBR 18.0, 17.3 LTS, 17.2, 16.4 LTS, 15.4 LTS, 14.3 LTS, 13.3 LTS.
**DBR 18.1 entered Beta** — Apache Spark 4.1.0.

### Developer Tools

- Databricks Apps: Git repository deployment (Beta), app tagging (Public Preview), MCP server integration.
- Power BI connections now use ADBC driver by default (existing ODBC connections unchanged).
