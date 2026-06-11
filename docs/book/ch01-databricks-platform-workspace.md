# Chapter 1: The Databricks Platform & Workspace

> **Source:** DA-FREE v3.1.1 — M1: Databricks Workspace Walkthrough
> **Added:** 2026-06-11

## What you'll learn

- How the Databricks workspace is structured and how to navigate it
- The difference between compute types and when to use each
- How Unity Catalog fits into the workspace as the governance layer
- How Git integration works via Git folders
- How Serverless compute differs from classic clusters

## The problem this solves

Databricks provides a unified analytics platform that combines data engineering, SQL analytics, machine learning, and AI in a single workspace. Without knowing how the workspace is structured, every task — finding a table, attaching a cluster, granting permissions, connecting a Git repo — requires trial-and-error. This chapter gives you the mental map so you can orient yourself immediately in any Databricks workspace.

## Core concept

The Databricks workspace is an environment hosted in the **Control Plane** — the managed cloud service run by Databricks — that connects to your organisation's **Data Plane** (your cloud storage, compute, and networking). As a user, you interact with the Control Plane; your data never leaves your cloud account.

The workspace has a left sidebar with sections for different activities:

```
+ New          → create any asset (notebook, job, cluster, warehouse…)
Workspace      → file browser for notebooks and folders
Catalog        → Unity Catalog browser (tables, volumes, functions, models)
Jobs & Pipelines → Lakeflow Jobs and Declarative Pipelines
Compute        → clusters, SQL Warehouses, pools, policies
SQL            → SQL Editor, Dashboards, Genie
Data Engineering → Runs, Data Ingestion
```

**Unity Catalog** is the governance layer. Every table, view, function, model, and volume lives in a three-level namespace: `catalog.schema.object`. The Catalog Explorer in the sidebar lets you browse this hierarchy, inspect table schemas, manage permissions, and view lineage — all without writing SQL.

**Compute** is split into types:

| Type | Use case | Billing |
|------|----------|---------|
| All-Purpose | Interactive notebooks | All-Purpose DBU rate |
| Job Compute | Scheduled jobs | Job DBU rate (~70% cheaper) |
| SQL Warehouse | SQL Editor, dashboards | SQL DBU rate |
| Serverless | Notebooks, jobs, SQL | Per-second, fully managed |
| Vector Search | Embedding index queries | Dedicated DBU |

The key insight: **Serverless compute is the default** for notebooks on modern workspaces. You attach to it immediately — no cluster startup time. Under the hood, Databricks manages the infrastructure; you just pay for the seconds you actively use it.

**Photon** is a C++ vectorised query engine that replaces the JVM-based Spark execution engine for SQL and DataFrame operations. It's enabled at the cluster level and delivers significant speedups for aggregations, sorts, and joins. It does *not* accelerate Python UDFs, which still run on the JVM/Python interpreter.

## Code examples

### Setting the default catalog and schema

In any notebook, use `USE CATALOG` and `USE SCHEMA` to avoid typing fully-qualified names on every query:

```sql
USE CATALOG my_catalog;
USE SCHEMA my_schema;

-- Now all unqualified table names resolve to my_catalog.my_schema
SELECT * FROM my_table;
```

In PySpark (Spark 3.4+):

```python
spark.catalog.setCurrentCatalog("my_catalog")
spark.catalog.setCurrentDatabase("my_schema")
```

### Granting permissions via SQL

```sql
-- Grant SELECT to all authenticated users in the account
GRANT SELECT ON TABLE wine_quality_table TO `account users`;

-- Verify
SHOW GRANTS ON TABLE wine_quality_table;
```

The same grant can be done through the Catalog Explorer: **Catalog → table → Permissions tab → Grant**.

### Listing compute in a notebook

```python
# Check which cluster/compute is currently attached
print(spark.conf.get("spark.databricks.clusterUsageTags.clusterId"))
print(spark.conf.get("spark.databricks.clusterUsageTags.clusterName"))
```

### Connecting a Git folder

```
Workspace → + New → Git folder
→ Paste repo URL (GitHub, GitLab, Bitbucket)
→ Authenticate via Settings → Developer → Linked Accounts
→ Create Git folder
```

After creation, right-click the folder → **Git** to pull, push, commit, or create branches.

## Best practices

- Use **Serverless compute** by default for interactive work. Switch to a classic cluster only if you need a specific library that isn't pre-installed, need GPU support, or need to configure Spark parameters that Serverless doesn't expose.
- Use **Job Compute** (not All-Purpose) for scheduled jobs. The DBU rate is ~70% cheaper, and production jobs should have their own isolated cluster.
- Pin frequently used notebooks to **Favorites** to avoid losing them in deep workspace hierarchies.
- Use **Git folders** instead of manually copying notebooks. Git folders give you version history, branching, and the ability to review changes before committing.
- Grant permissions at the **schema or catalog level** when possible, rather than table-by-table. It scales better as your data model grows.

## Common pitfalls

- **Attaching an All-Purpose cluster to a job task** generates a billing warning and charges the higher All-Purpose DBU rate. Always choose Job Compute or Serverless for job tasks in production.
- **Confusing Repos (legacy) with Git folders**: the legacy Repos feature has been replaced by Git folders. If you see "Repos" in the sidebar, it's the old UI. Use Git folders for new work.
- **Photon doesn't help Python UDFs**: if your bottleneck is a Python function applied row-by-row with `udf()`, Photon won't accelerate it. Rewrite as a native Spark/SQL expression to get the speedup.
- **Running notebooks as jobs without parameterisation**: hardcoded catalog/schema names in notebooks break when the same notebook is used in different environments. Use `dbutils.widgets` or job parameters.
- **Not setting `USE CATALOG`/`USE SCHEMA`** leads to tables being created in the wrong place. Always confirm `SELECT current_catalog(), current_schema()` at the start of a notebook.

## Exercises

1. **Recall** — What are the three levels of the Unity Catalog namespace, and what kind of objects exist at each level?
2. **Apply** — Open a Databricks workspace, create a new notebook, attach Serverless compute, run `SELECT current_catalog(), current_schema()`, and change the schema using `USE SCHEMA`.
3. **Extend** — Connect a GitHub repository as a Git folder and create a new notebook inside it. Commit the notebook and verify the commit appears in GitHub.

## Summary

- Databricks workspace = Control Plane (managed by Databricks) + Data Plane (your cloud).
- Unity Catalog governs all data objects in a `catalog.schema.object` three-level namespace.
- Compute is split into All-Purpose, Job, SQL Warehouse, and Serverless modes — each billed differently.
- Serverless is the default and the recommended starting point; switch to classic clusters only for specific needs.
- Git folders replace the legacy Repos feature for version-controlled notebook development.

The next chapter introduces Apache Spark's architecture and how it runs on Databricks clusters.
