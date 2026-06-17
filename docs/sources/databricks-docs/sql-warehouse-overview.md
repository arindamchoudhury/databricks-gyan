# SQL warehouse overview

> **Source:** [docs.databricks.com/aws/en/compute/sql-warehouse/](https://docs.databricks.com/aws/en/compute/sql-warehouse/)
> **Added:** 2026-06-16
> **Source updated:** 2026-01-08
> **Tags:** compute, sql-warehouse, serverless, databricks-sql, BI, B1
> **Type:** documentation

## Summary

Overview landing page for SQL warehouses — the SQL-optimised compute resource for querying and exploring data in Databricks SQL. Distinct from classic compute (all-purpose/job clusters): SQL warehouses are purpose-built for BI and analytics workloads. Databricks recommends serverless SQL warehouses when available. Detailed sizing, scaling, and configuration live on separate linked pages.

## Key points

- **SQL warehouse** = SQL-optimised compute for Databricks SQL; renamed from "SQL endpoint" in 2023.
- **Serverless recommended**: instant/elastic compute, no capacity management, lower TCO.
- **Starter Warehouse** auto-created in every workspace to get you going.
- **Auto-start**: querying a stopped warehouse starts it automatically (if you have access).
- **CAN MONITOR** permission needed to manually start; admin-level to create.
- **Unity Catalog** governs data access on SQL warehouses.
- Classic compute (all-purpose/job clusters) ≠ SQL warehouses — separate compute type, separate UI, separate permissions.

## Notes

### What a SQL warehouse is

"A SQL warehouse is a compute resource that lets you query and explore data on Databricks."

SQL warehouses appear in the compute drop-down menus of Databricks SQL workspace UIs (query editor, Catalog Explorer, dashboards). They are distinct from classic compute clusters — purpose-built for SQL analytics, not general Spark workloads.

> 💡 Naming history: "SQL endpoints" were renamed "SQL warehouses" in 2023. The two terms are equivalent; older documentation may still use "endpoint."

### Warehouse types

Three types exist (classic, pro, serverless), though the page focuses on serverless:

**Serverless SQL warehouses** (recommended):

- **Instant and elastic compute** — no waiting for infra; no over-provisioning during spikes.
- **Minimal management** — capacity management, patching, upgrades, and performance optimisation handled by Databricks.
- **Lower TCO** — automatic provisioning/scaling avoids over-provisioning and reduces idle time.

"Databricks recommends using serverless SQL warehouses when available."

> 💡 Sizing, scaling, queuing, auto-stop, channels, and Photon configuration are covered on separate linked pages not yet captured.

### Starter Warehouse

"To help you get started, Databricks creates a small SQL warehouse called **Starter Warehouse** automatically."

Every workspace gets a small pre-created warehouse. Useful for initial exploration without needing admin intervention.

### Starting a warehouse

"Running a query against a stopped warehouse starts it automatically if you have access to the warehouse."

Auto-start is also triggered by: scheduled jobs, JDBC/ODBC connection establishment, and associated dashboards opening.

Manual start: requires **CAN MONITOR** permission → click SQL Warehouses in the sidebar.

### Creating a warehouse

"Configuring and launching SQL warehouses requires elevated permissions generally restricted to an administrator."

"Unity Catalog governs data access permissions on SQL warehouses for most assets. Administrators configure most data access permissions."

### Connecting third-party tools

**BI tools**: Power BI, Tableau (and others via JDBC/ODBC).

**Developer tools**: REST API, Databricks CLI, Python SQL Connector, SQLTools Driver for VS Code, DataGrip, DBeaver, SQL Workbench/J.

## Open questions

- ❓ What are the size options for SQL warehouses (2X-Small → 4X-Large etc.) and what do they control?
- ❓ What is the full permission model for SQL warehouses (CAN USE, CAN MONITOR, CAN MANAGE)?
- ❓ How does classic vs pro vs serverless warehouse differ in capability and cost?
- ❓ What are the auto-stop, min/max cluster, and channel (current vs preview) configuration options?

## Related sources

- [[classic-compute-overview]] — all-purpose/job compute; different compute type from SQL warehouses.
- [[serverless-notebooks]], [[serverless-jobs]], [[serverless-pipelines]] — serverless classic compute; SQL warehouses are separately serverless.
- [[serverless-limitations]] — limitations on serverless classic compute (not SQL warehouses).
