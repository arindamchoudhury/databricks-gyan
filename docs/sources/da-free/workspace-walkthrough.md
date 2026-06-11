# M1: Databricks Workspace Walkthrough

> **Source:** DA-FREE v3.1.1 — `M1 - Databricks Overview/01 - Databricks Workspace Walkthrough.ipynb`
> **Added:** 2026-06-11
> **Tags:** workspace, UI, compute, unity-catalog, notebooks, B1
> **Type:** notebook

> 📌 **Full explained chapter:** [[ch01-databricks-platform-workspace]]

## Summary

A UI walkthrough of the Databricks Data Intelligence Platform. Covers homepage navigation, left sidebar, user settings, notebook interaction, Unity Catalog via Catalog Explorer, and the available compute types. Minimal coding — primarily a tour of the interface.

## Key points

- The workspace homepage has tabs: Suggested, Favorites, Popular, Mosaic AI, What's New.
- Left sidebar top items: + New, Workspace, Recents, Catalog, Jobs and Pipelines, Compute, Discover, Marketplace — plus SQL, Data Engineering, and AI/ML sections.
- Notebooks default to **Serverless compute**. You can switch to a classic cluster via the dropdown.
- Unity Catalog permissions can be managed via the Catalog Explorer UI or SQL `GRANT` statements.
- Compute is grouped into: All-Purpose, Job Compute, SQL Warehouses, Vector Search, Pools, Policies.
- **Photon** is a C++ vectorized engine for SQL and DataFrame operations — enabled at the cluster level.
- Git integration uses **Git folders** (not the legacy Repos feature).

## Notes

### Homepage

The Databricks logo (top-left) navigates to the welcome screen with five tabs:

- **Suggested** — recently opened assets
- **Favorites** — starred notebooks, tables, any asset
- **Popular** — assets frequently accessed by coworkers in the last 30 days
- **Mosaic AI** — recently added and featured AI models in Model Serving
- **What's New** — platform announcements; can create objects directly from announcements

Search at the top is powered by **DatabricksIQ** — fuzzy, contextual, filter-able by asset type.

### Left sidebar navigation

**Top-level items**

- **+ New** — create notebook, query, dashboard, job, ETL pipeline, alert, model, app, cluster, SQL Warehouse, Git folder
- **Workspace** — file browser; supports drag-and-drop for organizing notebooks and files
- **Recents** — recently visited files and folders
- **Catalog** — browse Unity Catalog hierarchy
- **Jobs and Pipelines** — Lakeflow Jobs and Spark Declarative Pipelines
- **Compute** — manage clusters, SQL Warehouses, instance pools, policies

**SQL section**

SQL Editor, Queries, Dashboards, Genie Spaces, Alerts, Query History, SQL Warehouses.

**Data Engineering section**

Runs, Data Ingestion.

### Notebooks

- Language switcher per cell (Python, SQL, R, Scala) or use `%py`, `%sql`, `%r`, `%scala` magic commands
- `%md` for markdown cells
- Left sidebar icons: Table of Contents, folder view, Catalog browser
- Right sidebar icons: Comments, MLflow Experiments, Version History, Variables, Environment, Info, Genie Code
- **Genie Code** — AI assistant for generating code and diagnosing errors (Command/Alt + I)
- Run all: **Run all** button; run cell: **Shift + Enter** or Run button

### Unity Catalog permissions — two paths

**Via UI (Catalog Explorer)**

```
Catalog → table → Permissions tab → Grant → select user/group → choose privilege (SELECT / MODIFY) → Grant
```

**Via SQL**

```sql
GRANT SELECT ON TABLE `wine_quality_table` TO `account users`;
SHOW GRANTS ON TABLE `wine_quality_table`;
```

### Compute types

| Type | Use case |
|------|----------|
| All-Purpose | Interactive notebooks, ad-hoc exploration |
| Job Compute | Scheduled jobs (lower DBU cost than All-Purpose) |
| SQL Warehouses (Serverless / Classic) | Databricks SQL queries and dashboards |
| Instance Pools | Pre-warmed instances to reduce cluster startup time |
| Vector Search | Dedicated compute for embedding index queries |

**Serverless compute** is the default. It handles infrastructure automatically and bills per-second of active work.

**Photon** is enabled at the cluster level on All-Purpose and Job clusters. It accelerates SQL aggregations, sorts, and joins. Does not accelerate Python UDFs.

**Databricks Runtime** versions: standard (Spark + Delta + common libs), ML Runtime (adds pre-installed ML libraries, AutoML, GPU support).

### Git folders

Git folders (not legacy Repos) connect a workspace folder to a Git provider (GitHub, GitLab, Bitbucket). Credentials set in **Settings → Developer → Linked Accounts**.

```
Workspace → Create → Git folder → paste repo URL → Create Git folder
```

Pull/push/commit via right-click on the Git folder → **Git**.

## Related sources

- [[ch01-databricks-platform-workspace]] — full explanatory chapter
- [[creating-delta-table]] — first hands-on demo using the workspace
