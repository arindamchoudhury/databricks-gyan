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

## Running a local notebook on Databricks

> **Worked example:** [`notebooks/intro.ipynb`](../../notebooks/intro.ipynb) — a word-count notebook adapted from the local Spark environment. The original reads a local file and creates its own `SparkSession`; the Databricks copy applies all three changes below.

A notebook written for a local Spark installation needs three changes before it will run on Databricks.

### 1. Remove the SparkSession block

On Databricks, `spark` is pre-created and injected into every notebook automatically. Any `SparkSession.builder` block — along with local-only setup such as `os.environ["SPARK_LOCAL_IP"]`, log4j config paths, and custom UI ports — must be removed entirely:

```python
# Remove this whole block — Databricks provides spark for you
import os
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

spark = (
    SparkSession.builder
    .appName("my-app")
    .config("spark.ui.port", "4041")
    ...
    .getOrCreate()
)
```

After removing it, `spark` just works in every cell.

### 2. Fix local file paths

Local paths (`../data/file.txt`, `C:/Users/...`) don't exist on a Databricks cluster. Three options in order of convenience:

| Option | When to use |
|--------|-------------|
| Download inline with `urllib` | Small public files (Project Gutenberg, sample data) |
| Unity Catalog Volume (`/Volumes/catalog/schema/vol/file`) | Team data, persistent across sessions |
| DBFS (`/dbfs/FileStore/...`) | Legacy; prefer UC Volumes on modern workspaces |

**Unity Catalog Volume example** (recommended — persists across sessions, works on all compute types):

```python
# Create the UC hierarchy once
spark.sql("CREATE CATALOG IF NOT EXISTS learning")
spark.sql("CREATE SCHEMA IF NOT EXISTS learning.chap1")
spark.sql("CREATE VOLUME IF NOT EXISTS learning.chap1.intro")

# Download the file into the volume
import urllib.request
urllib.request.urlretrieve(
    "https://www.gutenberg.org/files/1342/1342-0.txt",
    "/Volumes/learning/chap1/intro/1342-0.txt",
)

# Read — no file: prefix needed
book = spark.read.text("/Volumes/learning/chap1/intro/1342-0.txt")
```

UC Volumes are the correct Databricks-native storage for files. The `/Volumes/<catalog>/<schema>/<volume>/` path works directly in `spark.read` without any URI prefix. Avoid `file:/tmp/` — Databricks restricts local filesystem access to `/Workspace` paths only.

### 3. Remove `spark.stop()`

`spark.stop()` terminates the shared cluster context — it kills the compute for every user attached to that cluster. Remove it unconditionally. Databricks manages the cluster lifecycle; you never stop Spark manually.

### Importing the notebook into the workspace

**Via the UI (simplest):**

```
Workspace → (navigate to target folder) → ⋮ menu → Import
→ Select File → choose the .ipynb file → Import
```

The notebook appears in the folder immediately, ready to attach compute and run.

**Via the Databricks CLI** (useful for scripting or CI):

```bash
databricks workspace import /Users/you@example.com/intro \
  --file notebooks/intro.ipynb \
  --format JUPYTER \
  --overwrite
```

The current CLI is the Go-based binary from [github.com/databricks/cli](https://github.com/databricks/cli) (v1.3.0, 2026-06-10) — **not** the legacy `databricks-cli` pip package (deprecated Oct 2023).

Install:

```bash
# Windows
winget install Databricks.DatabricksCLI

# macOS / Linux
brew tap databricks/tap && brew install databricks
```

Authenticate (OAuth U2M — opens a browser):

```bash
databricks auth login --host https://<your-workspace>.cloud.databricks.com
```

URL format by cloud:

| Cloud | Workspace URL |
|-------|--------------|
| AWS (incl. Free Edition) | `https://<workspace>.cloud.databricks.com` |
| Azure | `https://<workspace>.azuredatabricks.net` |
| GCP | `https://<workspace>.gcp.databricks.com` |

**Databricks Free Edition** runs on AWS — sign up at `login.databricks.com`. Community Edition retired January 1, 2026.

Use `databricks configure --token` only if your workspace does not support OAuth.

**Managing multiple profiles.** Each `auth login` saves a named profile to `~/.databrickscfg`. Commands without `-p` use the `DEFAULT` profile — if that profile is stale or points to a different workspace, authentication fails. List all configured profiles:

```bash
databricks auth profiles
# DEFAULT            https://dbc-....cloud.databricks.com  NO   ← stale
# my-workspace       https://dbc-....cloud.databricks.com  YES
```

To make a workspace the default, re-run auth and accept `DEFAULT` as the profile name:

```bash
databricks auth login --host https://<your-workspace>.cloud.databricks.com
# Profile name prompt → press Enter (saves as DEFAULT)
```

Or pass `-p <profile-name>` on every command to use a named profile explicitly.

### Running the notebook

1. Open the imported notebook.
2. Click **Connect** (top-right) → select **Serverless** or an All-Purpose cluster.
3. Click **Run all**, or `Shift+Enter` through cells.

Serverless attaches in seconds with no cluster startup wait. Use an All-Purpose cluster only if you need custom libraries or Spark configuration not available on Serverless.

## Running notebooks from VS Code

The Databricks extension for VS Code lets you run notebooks on your workspace directly from a local folder — no manual import required.

### Installation & configuration

1. Install the **Databricks** extension (by Databricks Inc.) from the VS Code Extensions panel.
2. Open a folder in VS Code (`File → Open Folder`), then click the Databricks icon in the sidebar.
3. The panel shows **"Databricks project configuration was not detected"** with three buttons:
   - **Create configuration** — creates a `.databricks/project.json` in the current folder and walks you through selecting a workspace host and cluster. **Start here.**
   - **Select a project** — points to an existing configured folder.
   - **Create a new project** — scaffolds a new project from a template.
4. Click **Create configuration** → select your workspace from the dropdown (pulled from `~/.databrickscfg`) → select or create a cluster.

### Open your course or project folder

```
File → Open Folder → C:\opt\learn\databricks\courses\<course-folder>
```

All notebooks in the folder are immediately available. No import step needed.

### Two execution modes

#### Interactive — cell by cell (Databricks Connect)

Spark operations execute on the cluster; all other code runs locally. Feels identical to a local Jupyter notebook.

- Requires a **classic All-Purpose cluster** running DBR 13.3 or above.
- **Does not work with Serverless compute.**
- Install Databricks Connect inside the extension when prompted.
- Open any `.ipynb` → run cells with the standard notebook toolbar.
- `spark`, `dbutils`, `display`, and `sql` are pre-injected — no setup code needed.

#### Run as Job

Submits the whole notebook as a Lakeflow Job run. Works with any compute including Serverless.

Open the `.ipynb` → click the **Run on Databricks** icon in the title bar → **Run File as Workflow**. Results appear in a "Databricks Job Run" tab; click the run ID to open the full job detail in the workspace UI.

### Creating an All-Purpose cluster for Databricks Connect

If you only have Serverless, create a classic cluster for interactive work:

```
Databricks UI → Compute → Create compute
→ Runtime: 18.x (Spark 4.1, Scala 2.13)
→ Node type: smallest available (e.g. i3.xlarge)
→ Auto-terminate: 30 min
→ Create
```

Attach this cluster in the VS Code Databricks sidebar before running cells interactively.

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
- **Using `file:/tmp/` paths in `spark.read`**: Databricks restricts local filesystem access to `/Workspace` paths only. `spark.read.text("file:/tmp/...")` raises `LocalFilesystemAccessDeniedException`. Use a UC Volume path (`/Volumes/catalog/schema/volume/file`) instead — it works on all compute types without any URI prefix.
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
