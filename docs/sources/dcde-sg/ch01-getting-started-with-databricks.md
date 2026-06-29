# Ch 1 — Getting Started with Databricks

> **Source:** Derar Alhussein, *Databricks Certified Data Engineer Associate Study Guide* (O'Reilly, 1st Ed., Feb 2025) — Chapter 1, PDF pp. 20–113.
> **Added:** 2026-06-14
> **Tags:** lakehouse, architecture, control-plane, data-plane, spark, dbfs, clusters, notebooks, dbutils, git-folders, B1
> **Type:** book

> *A scene-setting chapter: what the Databricks lakehouse is, its four-layer architecture, the control/data plane split, Spark + DBFS, and a hands-on tour of the workspace — clusters, notebooks, magic commands, `dbutils`, versioning, and Git folders.*

> 📌 **Notes adapted to the 2026 platform.** The book targets the older DCDEA exam aligned to **DBR 13.3 LTS** and references **Community Edition**. Concepts are unchanged, but several names/defaults moved on by mid-2026 — flagged inline with ⚠️ and summarized in [research-cache](../../research-cache/dcde-sg-ch01-facts/). Key shifts: access modes renamed **Standard/Dedicated**, **Community Edition → Free Edition**, **DBFS deprecated** in favor of UC Volumes, **DLT → Lakeflow Spark Declarative Pipelines**.

> 📎 **Overlaps:** the personal book chapter [[ch01-databricks-platform-workspace]] (full explanatory version) and the course note [[workspace-walkthrough]] (DA-FREE M1) cover the same ground.

---

## 1. Introducing the Databricks Platform

The pitch: traditional stacks force a split between **data lakes** (cheap, flexible, but weak on quality/governance) and **data warehouses** (structured, performant, but rigid and costly). Running both means duplication, constant data movement, and fractured governance. The **data lakehouse** unifies them in one place.

- **Databricks Data Intelligence Platform** = an AI-powered data lakehouse built on Apache Spark.
- A lakehouse combines lake **openness/scalability/cost** with warehouse **reliability/governance/performance**.
- One platform for data engineering, ML, and analytics — engineers, scientists, and analysts work together on the same data.

> 💭 (mine): the book's analogy — a disorganized storage shelf (lake) vs. a curated library (warehouse) vs. a smart adaptable library (lakehouse). Fine for intuition; the load-bearing idea for the exam is *one copy of data, governed once, serving BI + AI*.

---

## 2. High-level architecture — four layers

Bottom to top:

| Layer | Role |
|---|---|
| **Cloud infrastructure** | Multi-cloud (Azure, AWS, GCP). Provides storage, networking, and the VMs/nodes that run clusters. |
| **Databricks Runtime (DBR)** | Pre-configured VM image: Apache Spark + Delta Lake + system libraries. (Delta Lake → Ch 2.) |
| **Data governance — Unity Catalog** | Centralized governance across all data & AI assets; access control, security, lineage. (UC → Ch 8.) |
| **Workspace** | The UI layer — notebooks, dashboards, workflows; multi-language (Python, SQL, R, Scala). |

> 💡 The exam likes "which layer does X?" — DBR = the runtime image, UC = governance, workspace = the UI you click in.

---

## 3. Deployment — control plane vs. data plane

When Databricks is deployed into your cloud, it splits into two planes (this is the single most exam-relevant diagram in the chapter):

- **Control plane** — *managed by Databricks*, lives in the Databricks account. Hosts the UI, cluster manager, workflow/job service, notebooks, REST API, and CLI. Handles workspace management, cluster provisioning, job scheduling.
- **Data plane** — *in the customer's own cloud subscription*. Where **classic (non-serverless) compute** VMs and **storage** actually live. When you spin up a Spark cluster, those VMs land here; DBFS / UC storage lives here too.

Why the split matters:

- Compute + data stay in the customer's cloud → customer keeps control over security/compliance.
- Databricks can update/maintain the platform without touching customer data/compute.

> ⚠️ **Exam trap (verified):** *"Which location hosts the customer data?"* → the **customer's own cloud account** (the data plane), **not** the control plane / Databricks account. (Book's Sample Question 1; answer in its Appendix C.)

> 📌 **Serverless caveat:** the "data plane in your account" rule holds for *classic* compute. Serverless compute runs in a Databricks-managed plane. The book is classic-compute-centric.

---

## 4. Apache Spark on Databricks

Spark is the open-source distributed processing engine at the core; Databricks was founded by Spark's original creators and ships a heavily optimized Spark.

Key features called out:

- **Distributed processing** — parallel work across cluster nodes, scaled up/down with cloud clusters.
- **In-memory processing** — keeps data in memory across the cluster; big win for iterative/complex jobs.
- **Multi-language** — Scala, Python, SQL, R, Java.
- **Batch + stream** — historical transforms *and* real-time/continuous streams.
- **Flexible data** — structured, semi-structured, unstructured (CSV, JSON, images, video, nested types).

> 💭 (mine): all review if you've done core Spark — see the Spark notes. The Databricks-specific delta here is just "optimized Spark + cloud-elastic clusters."

### Databricks File System (DBFS)

- An **abstraction layer** over cloud storage — interact with cloud files as if local.
- A file written to DBFS is actually persisted in the underlying cloud store (e.g., DBFS on Azure → **ADLS**), so it survives cluster termination.

> ⚠️ **Outdated (2026):** **DBFS root and mounts are deprecated.** New workspaces are **Unity Catalog–only** (all new Azure workspaces UC-only from **Sep 30, 2026**). Use **UC Volumes** (`/Volumes/<catalog>/<schema>/<volume>/`) for user data. The read-only `/databricks-datasets/` sample path still works.

---

## 5. Setting up a workspace

- Needs an active Databricks account; a **14-day free trial** runs on your own Azure/AWS/GCP account.
- Cloud-specific setup steps live in the book's Appendix A — but **the exam has no cloud-specific questions** (you won't be tested on per-cloud workspace creation).

> ⚠️ **Outdated (2026):** the book points learners without a cloud account to **Community Edition** (Appendix B). CE was **retired Jan 1, 2026** → use **[Databricks Free Edition](https://login.databricks.com)** (perpetual, serverless, no cloud account needed; runs on AWS). See [[feedback-databricks-platform-facts]].

---

## 6. Exploring the workspace UI

Two regions: **sidebar** (left) and **top bar**.

### Sidebar

- **Common:** *Workspace* (browser for folders/notebooks/files), *Catalog* (data & AI assets), *Workflows* (jobs/orchestration), *Compute* (clusters & pools).
- **SQL** → Databricks SQL (analytics/reporting; Ch 7). ⚠️ Book notes "not in Community Edition" — moot now (CE retired).
- **Data Engineering** → ingestion, pipelines, jobs (Ch 6).
- **Machine Learning** → experiments, feature store, model serving. *Not on the DE Associate exam.*

### Top bar

- **Search** (AI-powered, natural language across tables/notebooks/dashboards), **Switch Workspaces**, **Databricks Assistant** (AI helper for code gen/explain/debug; UC-aware), **Profile settings** (prefs, linked accounts, admin).

### Workspace browser

Hierarchical file tree. Key directories:

- **Home** — your personal default location (semi-private).
- **Workspace** — root containing all users' Home dirs (`Users > you@example.com`).
- **Repos** — *legacy* Git integration, **replaced by Git folders** (§9).
- **Trash** — deleted items, retained **30 days**.

Use **Create** (right side) to add folders/notebooks; the **⋮ menu** (three dots) handles import/export (e.g., import local code, export folder as archive).

---

## 7. Importing the book materials

Two methods to get the book's GitHub repo (`github.com/derar-alhussein/oreilly-databricks-dea`) into the workspace:

- **Option 1 — Git folder** (full Databricks): Create → *Git folder*, paste repo URL, it auto-detects the provider, Create. Repo appears as a navigable folder. *Public repos need no extra auth.*
- **Option 2 — DBC file** (⚠️ book's Community-Edition path): download `book_materials.dbc` from the repo's `Exports/` folder, then Workspace ⋮ → *Import* → upload the `.dbc`.

> 💡 `.dbc` (Databricks Cloud archive) is still a valid way to move notebook bundles between workspaces — useful even outside CE.

---

## 8. Clusters — concepts and types

A **cluster** = a set of nodes (VMs/instances) acting as one. Spark cluster = one **driver** node (orchestrates) + several **worker** nodes (execute tasks in parallel).

Two primary types:

| | **All-purpose cluster** | **Job cluster** |
|---|---|---|
| Usage | Interactive dev / EDA | Automated job execution |
| Management | Manually created & managed by user | Auto-created by the job scheduler |
| Termination | Manual or auto-terminate on idle | Auto-terminates when the task completes |
| Cost | Higher | Cheaper (ephemeral) |

- **All-purpose:** for notebooks, testing, ad-hoc analysis. Auto-termination saves cost but enforces a **10-minute minimum runtime**.
- **Job cluster:** ephemeral, spun up per job run, torn down after — recommended for production. (Used by Databricks Jobs and ⚠️ "DLT pipelines" → now **Lakeflow Spark Declarative Pipelines**; Ch 6.)

### Cluster pools

- A pool = a group of **pre-warmed, idle VMs** ready to attach to clusters.
- Benefit: cuts **cluster start time** and **autoscaling time** when nodes are available in the pool.
- ⚠️ Cost: Databricks doesn't charge for idle pool instances, **but your cloud provider does** — they're real running VMs. Balance speed vs. cloud cost.

---

## 9. Creating an all-purpose cluster (config walkthrough)

Compute tab → *All-purpose compute* → **Create compute**. Key settings in order:

1. **Name** — e.g., "Demo Cluster".
2. **Policy** — default *Unrestricted*; governed orgs may constrain settings.
3. **Single-node vs. multi-node** — single-node = driver only (driver does worker duties too; cheapest); multi-node = 1 driver + N workers (parallelism).
4. **Access mode** — book: *Shared* (multi-user, SQL+Python only) vs. *Single user* (dedicated to you).
   > ⚠️ **Renamed (2026):** **Shared → Standard**, **Single user → Dedicated**. Dedicated can now also be group-assigned and supports ML runtime, RDD APIs, R/Scala that Standard restricts.
5. **Databricks Runtime version** — book picks **DBR 13.3 LTS** to match the then-current exam.
   > ⚠️ **Current (2026):** **DBR 18** (Spark 4.1.0) / **DBR 17.3 LTS** (Spark 4.0.0). The new DCDEA exam version goes live **May 4, 2026** — check which DBR it aligns to before studying version-specific behavior.
6. **Photon** — optional C++ vectorized query engine; accelerates SQL-heavy / many-file workloads at extra cost.
7. **Worker nodes** — pick VM size (CPU/mem/storage); **autoscaling** on by default (set min/max workers) or fix a count (e.g., 3).
8. **Driver node** — match workers or configure separately.
9. **Auto-termination** — on by default; shut down after N idle minutes (e.g., 30) to avoid idle charges.
10. **Review** — right-side summary shows total worker cores, RAM, runtime, and **DBUs** (Databricks Unit = processing capacity/hour, the basis for cost). Single-node consumes fewer DBUs than multi-node.
11. **Create** — provisions VMs, applies config, installs DBR + libraries.

> ⚠️ **Quota note (book):** Azure free tier caps at **4 cores** — use a single-node cluster ≤ 4 cores to avoid a quota error. (On Free Edition you use serverless, so this classic-cluster limit doesn't apply.)

> 📌 **Serverless for notebooks:** runs code with no infra to configure; requires a UC-enabled workspace with serverless enabled in the account.

---

## 10. Managing a cluster

- A solid **green circle** next to the name = running.
- From the **Compute** list: start/stop via play/stop button; ⋮ menu → clone, edit permissions, delete.
- Click the name → edit config (instance type, worker count, Photon). Config changes **may require a restart** (interrupts running jobs).
- Monitoring/troubleshooting tools (on the cluster config page):
    - **Event log** — created/terminated/edited/errors.
    - **Spark UI** — jobs, stages, tasks; performance & bottlenecks.
    - **Driver logs** — stdout/stderr from notebooks & libraries on the driver.

---

## 11. Working with notebooks

Interactive, multi-language (Python/SQL/Scala/R), collaborative; integrate directly with Spark clusters. More capable than plain Jupyter.

- **Create:** Workspace → Create → *Notebook* (opens "Untitled Notebook"; rename via the title).
- **Default language** is Python; change via the language indicator at the top (per-notebook).
- **Attach compute:** *Connect* (top-right) → pick a cluster; selecting a terminated cluster auto-starts it (can take minutes).
- **Cells:** run individually — play button or **Shift+Enter** (runs current, moves to next). Output appears directly below; rich displays, errors, tooltips show inline.
- **Manage cells:** hover below a cell → **+ Code** to insert.

---

## 12. Magic commands

Special cell directives prefixed with `%`.

- **Language magics** — run one cell in a non-default language without changing the notebook:

    ```sql
    %sql
    SELECT "Hello world from SQL!"
    ```

  Databricks auto-prepends `%sql` when it detects SQL; the cell's language indicator updates. Languages: `%python`, `%sql`, `%scala`, `%r`.

- **`%md` — Markdown** for rich text/docs inside the notebook:

    ```text
    %md
    # Title 1
    ## Title 2
    ```

  Bonus: Markdown headers auto-populate the notebook's **table of contents** (left panel) for quick navigation.

- **`%run`** — execute another notebook inline; all its variables/functions/classes become available in the caller. Great for shared setup/config:

    ```python
    %run ./Setup        # ./ = current directory; or use a full workspace path
    ```

  Example pattern: a `Setup` notebook defines `book_publisher = "OReilly"`; after `%run ./Setup`, the caller can read `book_publisher`.

- **`%fs`** — quick file-system ops in a cell:

    ```text
    %fs ls '/databricks-datasets'   # lists ~55 sample datasets
    ```

---

## 13. Databricks Utilities (`dbutils`)

A richer, programmatic alternative to `%fs` — usable inside Python code.

```python
dbutils.help()           # all utilities
dbutils.fs.help()        # file-system commands

files = dbutils.fs.ls("/databricks-datasets/")   # returns a list, stored in a var
```

### Displaying output

```python
print(files)     # hard to read
display(files)   # tabular: filename, size, type — plus CSV download & chart viz
```

> ⚠️ `display()` previews only a **subset** of large datasets.

### `%fs` vs `dbutils` — when to use which

- **`%fs`** — quick one-off file ops; simplest.
- **`dbutils`** — when you need to capture output in a variable, branch/loop, or integrate with Python logic.

> ⚠️ **Exam trap (verified):** a **SQL notebook** running `files = dbutils.fs.ls(...)` + `print(files)` raises a *syntax error* because the cell runs as SQL. Fix = **add `%python` at the top of the cell** (Book Sample Q2; answer in its Appendix C). Swapping `print`→`display` does **not** fix it — that's still Python in a SQL cell.

---

## 14. Notebooks: export & built-in versioning

- **Export** (File → Export): *Source file* → `.py` script; *IPython Notebook* → `.ipynb`/HTML for sharing. Re-importable into any workspace via folder ⋮ → Import.
- **Version history** (right sidebar icon): chronological list of **auto-saved** versions; select one → *Restore this version* to revert.
- ⚠️ Limits: no branching/merging; history can be deleted by users → unreliable for serious version control. Use Git instead.

---

## 15. Git integration with Git folders

**Git folders** (formerly **Repos**) bring real Git workflows — branch, commit, push, pull — into the workspace.

- **Public repos** clone with no setup. **Private repos / push** require linking your Git provider.
- ⚠️ Not available in Community Edition (book) — moot now; available on Free Edition.

### Setup

1. Profile icon → **Settings** → **Linked accounts**.
2. Pick provider (GitHub, Azure DevOps, Bitbucket).
3. For GitHub, prefer the **Databricks GitHub App** over a personal access token (PAT) — more secure; authorize + install, granting all or selected repos.

### Daily workflow

- **Create Git folder:** Create → *Git folder* → paste repo URL → Create. Current **branch name** shows next to the folder.
- **Branches:** click the branch indicator → Git dialog → *Create Branch* (e.g., `dev`); it activates immediately. Switch branches via the dropdown. Work in `dev` keeps `main` stable.
- **Commit & Push:** Git dialog shows changes → write a commit message → **Commit & Push** (saves locally + pushes to remote).
- **Pull Requests:** ⚠️ Git folders **can't create PRs** — do that on the provider (GitHub). Changes in `dev` aren't in `main` until a PR is merged.
- **Pull:** with `main` selected, click **Pull** to fetch+merge remote into your local copy. Pull regularly to minimize conflicts.

---

## 16. Summary (chapter takeaways)

- **Lakehouse** = lake economics + warehouse reliability/governance, on one Spark-based platform for DE/ML/BI.
- **Four layers:** cloud infra → Databricks Runtime → Unity Catalog (governance) → workspace (UI).
- **Control plane** (Databricks-managed: UI, scheduler, API) vs. **data plane** (your cloud: classic compute + storage). **Customer data lives in the data plane** — the chapter's #1 exam fact.
- **Clusters:** all-purpose (interactive) vs. job (ephemeral, cheaper, production); pools pre-warm VMs. Driver + workers; autoscaling & auto-termination control cost; **DBU** = the billing unit.
- **Notebooks:** multi-language, cell-based; **magic commands** (`%sql`/`%md`/`%run`/`%fs`) and **`dbutils`** (+ `display()`) are the everyday tools.
- **Versioning:** built-in history is weak; **Git folders** (ex-Repos) give real Git — but PRs happen on the provider, not in Databricks.

---

## 17. Open questions / revisit

- ❓ Which DBR does the **May 4, 2026** DCDEA exam align to? (Book pins 13.3 LTS for the prior version — re-check before exam.)
- ❓ On **Free Edition** (serverless-only), how do the classic-cluster config screens in §9 map? Likely most cluster-creation questions become serverless — confirm what the new exam still tests.

---

## 18. References

- Book GitHub repo: <https://github.com/derar-alhussein/oreilly-databricks-dea>
- 2026 DCDEA exam guide (May 4, 2026): <https://www.databricks.com/sites/default/files/2026-03/databricks-certified-data-engineer-associate-exam-guide-may-4-2026.pdf>
- Compute / access modes: <https://docs.databricks.com/aws/en/compute/configure>
- DBFS & Unity Catalog best practices: <https://docs.databricks.com/aws/en/dbfs/unity-catalog>
- Databricks Free Edition: <https://login.databricks.com>

## Related notes

- [[ch01-databricks-platform-workspace]] — personal book chapter (full explanatory version of this material)
- [[workspace-walkthrough]] — DA-FREE M1 course note on the same UI tour
- [research-cache](../../research-cache/dcde-sg-ch01-facts/) — verified 2026 deltas vs. the 2025 book
