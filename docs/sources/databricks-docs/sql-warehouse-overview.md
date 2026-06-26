# SQL warehouse overview

> **Source:** [docs.databricks.com/aws/en/compute/sql-warehouse/](https://docs.databricks.com/aws/en/compute/sql-warehouse/)
> **Added:** 2026-06-16
> **Source updated:** 2026-01-08
> **Tags:** compute, sql-warehouse, serverless, databricks-sql, BI, B1
> **Type:** documentation

> "A SQL warehouse is a compute resource that lets you query and explore data on Databricks."

SQL warehouses are the **SQL-optimised compute** for Databricks SQL — purpose-built for BI and analytics, distinct from classic compute (all-purpose/job clusters) with their own UI and permissions. They appear in the compute drop-downs of the Databricks SQL UIs (query editor, Catalog Explorer, dashboards), and Unity Catalog governs their data access. Databricks recommends **serverless** SQL warehouses when available.

> 💡 Naming history: "SQL endpoints" were renamed "SQL warehouses" in 2023 — the terms are equivalent; older docs may still say "endpoint."

## Warehouse types

Three types exist (classic, pro, serverless); the page focuses on **serverless** (recommended):

- **Instant and elastic compute** — no waiting for infra, no over-provisioning during spikes.
- **Minimal management** — capacity management, patching, upgrades, and performance optimisation handled by Databricks.
- **Lower TCO** — automatic provisioning/scaling avoids over-provisioning and reduces idle time.

See [[sql-warehouse-types]] for the full classic-vs-pro-vs-serverless comparison.

## Starter Warehouse

"To help you get started, Databricks creates a small SQL warehouse called **Starter Warehouse** automatically." Every workspace gets one — useful for initial exploration without admin intervention.

## Starting a warehouse

"Running a query against a stopped warehouse starts it automatically if you have access to the warehouse." Auto-start is also triggered by scheduled jobs, JDBC/ODBC connection establishment, and associated dashboards opening. Manual start requires **CAN MONITOR** permission.

## Creating a warehouse

"Configuring and launching SQL warehouses requires elevated permissions generally restricted to an administrator." Unity Catalog governs data access permissions for most assets, configured by administrators.

## Connecting third-party tools

- **BI tools:** Power BI, Tableau (and others via JDBC/ODBC).
- **Developer tools:** REST API, Databricks CLI, Python SQL Connector, SQLTools Driver for VS Code, DataGrip, DBeaver, SQL Workbench/J.

Related: [[sql-warehouse-types]], [[classic-compute-overview]], [[serverless-notebooks]], [[serverless-limitations]].
