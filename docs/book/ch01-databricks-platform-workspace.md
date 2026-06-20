# Chapter 1: The Databricks Platform & Workspace

> **Source:** DA-FREE v3.1.1 — M1: Databricks Workspace Walkthrough
> **Added:** 2026-06-11

## What you'll learn

- How the Databricks workspace is structured and how to navigate it
- The difference between compute types and when to use each
- How Unity Catalog fits into the workspace as the governance layer
- How Git integration works via Git folders
- How Serverless compute differs from classic clusters

## Introduction

Databricks provides a unified analytics platform that combines data engineering, SQL analytics, machine learning, and AI in a single workspace. Without knowing how the workspace is structured, every task — finding a table, attaching a cluster, granting permissions, connecting a Git repo — requires trial-and-error. This chapter gives you the mental map so you can orient yourself immediately in any Databricks workspace.

## What is a lakehouse?

Before the workspace mechanics, the idea the whole platform rests on. The **lakehouse** is an open architecture that puts data-**warehouse** management features — ACID transactions, schema enforcement, governance, BI — directly on top of low-cost cloud object storage in open formats (Parquet), the cheap and flexible storage of a data **lake**. It's "what you would get if you had to redesign data warehouses in the modern world," now that object stores are cheap and reliable ([Databricks, 2020](../sources/databricks-blog/what-is-a-lakehouse.md)).

It exists to kill a two-tier tax. The old pattern was a **data lake** (cheap, flexible, but no transactions, no quality enforcement, no isolation — can't safely mix batch + streaming) feeding **one or more data warehouses** (reliable and fast on structured data, but poor on unstructured/AI data and not cheap), plus specialised systems for streaming, graph, and images. Every hop means copying data between systems → staleness, latency, and two copies to operate. The lakehouse collapses that into **one system, one copy** serving SQL/BI, data science, ML, and streaming.

Eight features define it — the rest of this book is largely how Databricks delivers each one:

| Lakehouse feature | Where Databricks delivers it |
|---|---|
| Transaction support (ACID) | Delta Lake — *Ch 5* |
| Schema enforcement & governance | Delta Lake + Unity Catalog — *Ch 5, 14* |
| BI on source data | Databricks SQL + Photon — *Ch 15, 23* |
| Storage decoupled from compute | Compute model (this chapter) |
| Openness (open formats + APIs) | Parquet / Delta, UniForm — *Ch 5, 22* |
| Diverse data types | Unity Catalog volumes, unstructured data — *Ch 14* |
| Diverse workloads | One platform: ETL, SQL, ML — *whole book* |
| End-to-end streaming | Structured Streaming, Lakeflow — *Ch 9, 10* |

> 📎 Primary source: [What Is a Lakehouse? (Databricks, 2020)](../sources/databricks-blog/what-is-a-lakehouse.md) — the post that named the architecture. Branding has since moved to the **Data Intelligence Platform**, but the argument is unchanged.

## The Data Intelligence Platform at a glance

"Data Intelligence Platform" is the current name for the lakehouse plus an AI layer that learns your organisation's semantics — table/column descriptions, metrics, jargon, usage, and human feedback — so search, BI, and agents understand *your* business, not just generic SQL ([DIP-Dummies Ch 1, 3](../sources/dip-dummies/ch03-databricks-platform.md)). For orientation, the platform is a stack of surfaces sitting on one governed copy of data. You don't need all of them for data engineering — but knowing the map stops you reaching for the wrong tool.

| Layer | Surface | What it is | In this book |
|---|---|---|---|
| **Storage** | Open Data Lake | One copy in open formats — **Delta Lake** or **Apache Iceberg**, no lock-in | Ch 5, 12, 22 |
| **Governance** | **Unity Catalog (UC)** | One governance layer for data *and* AI: `catalog.schema.object`, ACLs, lineage, semantics | Ch 14 |
| **Engineering** | **Lakeflow** | Declarative ETL: **Connect** (ingest), **Spark Declarative Pipelines** (transform), **Jobs** (orchestrate) | Ch 8, 10, 13, 18 |
| **Analytics** | **Databricks SQL** + **Photon** | Serverless data warehouse for ETL + BI on governed data | Ch 15, 23 |
| **OLTP** | **Lakebase** | Postgres-based transactional DB for the agentic era (compute/storage split, sub-second instances) | awareness only |
| **AI/agents** | **Agent Bricks** | Build/evaluate/govern composable AI agents on your data (UC-governed, built-in LLM judges) | awareness only |
| **Self-serve BI** | **AI/BI Genie / Dashboards** | NL chatbot over your data (Genie) + self-serve dashboards | Ch 15 (Genie) |
| **Apps** | **Databricks Apps** | Deploy data/AI apps on serverless compute, governed by UC | awareness only |
| **Sharing** | **OpenSharing**, **Marketplace**, **Clean Rooms**, **Lakehouse Federation** | Share live data / query external sources with zero copy | Ch 22 |
| **Assist** | **Databricks Assistant** | Context-aware AI in notebooks/SQL editor — generate, document, debug | this chapter |

> 💡 The through-line is **Unity Catalog** — every surface above governs through it. "Learn UC once, it secures everything else" is the single highest-leverage idea in the platform. The newer AI surfaces (Lakebase, Agent Bricks, Apps) are out of scope for a data-engineering path but appear here so you recognise them; this book stays on the storage → governance → engineering → analytics spine.

## How the workspace is structured

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

**Photon** is a C++ vectorised query engine that replaces the JVM-based Spark execution engine for SQL and DataFrame operations. It's enabled at the cluster level and delivers significant speedups for aggregations, sorts, and joins. It does *not* accelerate Python UDFs, which still run on the JVM/Python interpreter. Photon is available on both classic clusters and SQL Warehouses (always on for Serverless SQL Warehouses). Chapter 23 covers its internals and cost trade-offs.

### Classic cluster access modes

All classic (non-serverless) clusters have an **access mode** that controls isolation and feature availability. This is one of the most exam-tested distinctions:

| Access mode | Users | RDD access | GPU | Spark config override | Lakeguard | Best for |
|---|---|---|---|---|---|---|
| **Standard** | Multi-user | ❌ | ❌ | ❌ (blocked) | ✅ (enforced) | Data engineering, SQL, most ETL |
| **Dedicated** | Single-user | ✅ | ✅ | ✅ | ❌ | ML workloads, GPU compute, RDD-dependent code |
| **No Isolation Shared** | Multi-user | ✅ | ❌ | Limited | ❌ | Dev/test only; not recommended for production |

**Standard access mode** (formerly "Shared") uses **Spark Connect** — a client-server model where each user's code runs in an isolated server process. This is what **Lakeguard** enforces: users cannot read each other's in-memory DataFrames or `SparkContext` state, cannot override Spark configuration at the cluster level, and cannot use RDD APIs. The tradeoff is automatic per-user isolation with no teardown — critical for multi-tenant environments.

**Dedicated access mode** (formerly "Single User") gives one user full Spark access — including `SparkContext`, `RDD`, GPU kernels, and arbitrary Spark config. Required for any code that still uses the RDD API or relies on GPU-accelerated ML libraries.

> ⚠️ **The Standard/Dedicated terminology is current as of 2025.** Older Databricks docs, courses, and the DCDE-SG book use "Shared" and "Single User". They are the same access modes under new names. The API name in Terraform (`data_security_mode`) still uses `"SINGLE_USER"` and `"USER_ISOLATION"` as string values.

### SQL Warehouse types

SQL Warehouses run SQL queries and power the SQL Editor, dashboards, and BI tool connections. Three types:

| Type | Cold start | Management | Best for |
|---|---|---|---|
| **Serverless** | ~1–3 sec | Fully managed | Interactive SQL, dashboards, most use cases |
| **Pro** | ~2–4 min | Self-managed | Databricks SQL + Lakeflow Pipelines as source |
| **Classic** | ~2–4 min | Self-managed | Legacy BI tool compatibility, predictable config |

Serverless SQL Warehouses always run on Photon. Pro is required when a SQL Warehouse is used as a data source for Lakeflow Spark Declarative Pipelines materialized views.

### Compute pools (instance pools)

Compute pools are a fleet of pre-allocated cloud instances that clusters draw from. They eliminate cold-start time: instead of launching new VMs, a cluster borrows pre-warmed instances from the pool and starts in seconds. Useful when you need many short-lived clusters (e.g., CI job runs) or when the 5–10 minute cluster start time is unacceptable for your SLA. Pools are optional infrastructure — most teams add them after hitting cold-start friction in production.

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

Spark operations execute on remote Databricks compute; all other code runs locally. Feels identical to a local Jupyter notebook.

- Works with **either a classic All-Purpose cluster** (DBR 13.3+) **or Serverless compute**. Serverless requires Databricks Connect **15.4 LTS or above** — pick a recent version and it works out of the box.
- Select serverless by setting `serverless_compute_id = "auto"` in your connection config (or the `DATABRICKS_SERVERLESS_COMPUTE_ID` env var) instead of pointing at a `cluster_id`.
- Install Databricks Connect inside the extension when prompted.
- Open any `.ipynb` → run cells with the standard notebook toolbar.
- `spark`, `dbutils`, `display`, and `sql` are pre-injected — no setup code needed.

> **Historical note:** early Databricks Connect "v2" (released with DBR 13.3 in 2023) targeted only classic clusters — serverless support arrived in the 15.x line. Notes written before mid-2024 often still claim serverless is unsupported; that restriction no longer applies.

#### Run as Job

Submits the whole notebook as a Lakeflow Job run. Works with any compute including Serverless.

Open the `.ipynb` → click the **Run on Databricks** icon in the title bar → **Run File as Workflow**. Results appear in a "Databricks Job Run" tab; click the run ID to open the full job detail in the workspace UI.

### Creating an All-Purpose cluster for Databricks Connect

Serverless is enough for most interactive work. Create a classic All-Purpose cluster only if you need a custom library, GPU support, or a Spark configuration that Serverless doesn't expose:

```
Databricks UI → Compute → Create compute
→ Runtime: 18.x (Spark 4.1, Scala 2.13)
→ Node type: smallest available (e.g. i3.xlarge)
→ Auto-terminate: 30 min
→ Create
```

Attach this cluster in the VS Code Databricks sidebar before running cells interactively.

## Notebook features you'll use daily

A Databricks notebook has four cell types: **Code** (Python, SQL, Scala, or R set by the `%lang` magic), **Markdown** (documentation), **Result** (output below each code cell), and **Visualization** (inline chart from a result). Switch language in a cell with `%python`, `%sql`, `%scala`, or `%r`.

### Databricks widgets — parameterising notebooks

Widgets add interactive input controls to a notebook and let you pass parameters from jobs or `%run` calls. Four types:

| Type | What it does |
|---|---|
| `text` | Free text input |
| `dropdown` | Pick one from a list |
| `combobox` | Pick from list or type a custom value |
| `multiselect` | Pick one or more from a list |

```python
# Create a dropdown (default CA; choices: CA, IL, MI, NY)
dbutils.widgets.dropdown("state", "CA", ["CA", "IL", "MI", "NY"])

# Read the value anywhere in the notebook
state = dbutils.widgets.get("state")

# SQL — use parameter markers (DBR 15.2+; protects against injection)
# SELECT * FROM orders WHERE state = :state
```

Widgets accept **string values only** — no integers or booleans. In SQL cells, use parameter markers (`:param_name`) instead of string interpolation to prevent SQL injection.

> ⚠️ **On-change behaviour:** the default widget action is **"Run Accessed Commands"** — it reruns only cells that call `dbutils.widgets.get()` for that widget. SQL cells are **not** rerun in this mode. Switch to "Run Notebook" if you need SQL cells to refresh on widget change.

For rich interactive Python controls (sliders, buttons, accordions), use **ipywidgets** instead. Key distinction: ipywidgets cannot pass parameters between notebooks or to jobs — use Databricks widgets for that.

### Sharing code: %run and workspace files

Two patterns for reusing code across notebooks:

**Workspace files** (recommended): store functions in a `.py` file in the workspace and `import` it like any Python module. Requires DBR 11.3 LTS+. Supports Git, version control, and IDE debugging.

**`%run`**: includes another notebook inline — all its functions and variables become available in the calling notebook's scope. Must be alone in its cell.

```python
# %run — must be the only thing in its cell
%run ./utils/transforms

# After %run, everything defined in transforms is in scope
result = my_transform_function(df)
```

For orchestrating separate execution (with parameter passing and return values), use `dbutils.notebook.run()` — but prefer Lakeflow Jobs for any production scheduling need. The key rule: **`%run` merges scopes; `dbutils.notebook.run()` starts a separate job.**

### Interactive debugger

The built-in Python debugger (DBR 14.3 LTS+ on Standard; 13.3 LTS+ on Dedicated; Serverless) lets you set breakpoints, step through code, and inspect variables live without `print()` statements.

Enable: Username → **Settings** → **Developer** → toggle **Python Notebook Interactive Debugger** on.

Start a debug session: **Run > Debug cell** or `Alt+Shift+D`. Execution pauses before each breakpointed line. The **Variable Explorer** (right sidebar) shows all in-scope values; the **Debug Console** (bottom) lets you execute Python in the current frame.

> ⚠️ Debug sessions auto-terminate after **30 minutes** idle. The debug console has a **15-second timeout** per execution and does not support `display()`.

## Best practices

- Use **Serverless compute** by default for interactive work. Switch to a classic cluster only if you need a specific library that isn't pre-installed, need GPU support, or need to configure Spark parameters that Serverless doesn't expose.
- Use **Job Compute** (not All-Purpose) for scheduled jobs. The DBU rate is ~70% cheaper, and production jobs should have their own isolated cluster.
- Pin frequently used notebooks to **Favorites** to avoid losing them in deep workspace hierarchies.
- Use **Git folders** instead of manually copying notebooks. Git folders give you version history, branching, and the ability to review changes before committing.
- Grant permissions at the **schema or catalog level** when possible, rather than table-by-table. It scales better as your data model grows.
- **Never use the notebook schedule button** to create a production job. The schedule button creates a job against the latest *working* copy of the notebook — unsaved edits included. Use Lakeflow Jobs pointing at the latest *committed* version in a Git folder instead.
- Store reusable functions in **workspace files** (`.py`), not in notebook cells. Files are importable, testable, and versionable; code buried in cells is none of those things.
- Use **Standard access mode** (not Dedicated) for all multi-user ETL workloads. Dedicated is for single-user ML and GPU work only — it doesn't enforce isolation between users.

## Common pitfalls

- **Attaching an All-Purpose cluster to a job task** generates a billing warning and charges the higher All-Purpose DBU rate. Always choose Job Compute or Serverless for job tasks in production.
- **Confusing Repos (legacy) with Git folders**: the legacy Repos feature has been replaced by Git folders. If you see "Repos" in the sidebar, it's the old UI. Use Git folders for new work.
- **Photon doesn't help Python UDFs**: if your bottleneck is a Python function applied row-by-row with `udf()`, Photon won't accelerate it. Rewrite as a native Spark/SQL expression to get the speedup.
- **Using `file:/tmp/` paths in `spark.read`**: Databricks restricts local filesystem access to `/Workspace` paths only. `spark.read.text("file:/tmp/...")` raises `LocalFilesystemAccessDeniedException`. Use a UC Volume path (`/Volumes/catalog/schema/volume/file`) instead — it works on all compute types without any URI prefix.
- **Running notebooks as jobs without parameterisation**: hardcoded catalog/schema names in notebooks break when the same notebook is used in different environments. Use `dbutils.widgets` or job parameters.
- **Using the wrong access mode for the workload**: attaching a Standard-mode cluster to code that calls `sc` (SparkContext) or `.rdd` methods fails with an access-denied error. Standard uses Spark Connect, which does not expose the `SparkContext`. Switch to Dedicated mode for RDD or GPU workloads.
- **Mixing Databricks widgets and ipywidgets expectations**: ipywidgets cannot pass values to jobs or between notebooks via `%run`. If a widget value needs to flow into a job parameter, use `dbutils.widgets`, not `widgets.IntSlider`.
- **Forgetting that widget "Run Accessed Commands" skips SQL cells**: if your notebook mixes Python widget reads and SQL cells, SQL cells will not re-execute when a widget value changes under the default on-change behaviour. Manually re-run SQL cells or switch to "Run Notebook" mode.
- **Not setting `USE CATALOG`/`USE SCHEMA`** leads to tables being created in the wrong place. Always confirm `SELECT current_catalog(), current_schema()` at the start of a notebook.

## Exercises

1. **Recall** — What are the three levels of the Unity Catalog namespace, and what kind of objects exist at each level?
2. **Apply** — Open a Databricks workspace, create a new notebook, attach Serverless compute, run `SELECT current_catalog(), current_schema()`, and change the schema using `USE SCHEMA`.
3. **Extend** — Connect a GitHub repository as a Git folder and create a new notebook inside it. Commit the notebook and verify the commit appears in GitHub.

## Summary

- Databricks workspace = **Control Plane** (managed by Databricks) + **Data Plane** (your cloud). Your data never leaves your cloud account.
- **Unity Catalog** governs all data objects in a `catalog.schema.object` three-level namespace. Every table, volume, function, and model lives here.
- Compute breaks into: **All-Purpose** (interactive, expensive), **Job Compute** (~70% cheaper, production jobs), **SQL Warehouse** (SQL/BI, three sub-types), and **Serverless** (per-second, no startup, recommended default).
- Classic clusters have an **access mode**: **Standard** (multi-user, Lakeguard-enforced isolation, no RDD, no GPU) vs **Dedicated** (single-user, full Spark including RDD and GPU).
- **Standard = "Shared" (old name), Dedicated = "Single User" (old name)** — same modes, renamed in 2025.
- Notebooks support four cell types and integrate deeply with **Databricks widgets** for parameterisation and **workspace files** for code reuse.
- `%run` merges another notebook's scope inline; `dbutils.notebook.run()` starts a separate job. Both are fallbacks to Lakeflow Jobs for anything production.
- Never schedule production jobs with the notebook schedule button — it targets the working copy, not the committed version.
- **Git folders** replace legacy Repos for version-controlled development.

## References

- [What Is a Lakehouse? — Databricks blog (2020)](../sources/databricks-blog/what-is-a-lakehouse.md) — primary source for the lakehouse architecture and its eight defining features (reading notes).

The next chapter introduces Apache Spark's execution model — drivers, executors, DAGs, stages, and tasks — and how Databricks extends it with AQE and Photon.
