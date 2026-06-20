# Chapter 25: DevOps — Testing & Multi-Environment Deployment

> 🚧 **Stub.** This chapter is not yet written. It holds **parked material** relocated from Ch 1 so nothing is lost — fold it into the full chapter when topic **E3** is completed.

## Parked: local development with VS Code & Databricks Connect

A core DevOps practice is developing and testing locally in an IDE before deploying. The Databricks VS Code extension + Databricks Connect make the local loop feel like a native notebook while Spark runs on remote compute. This detail was moved here from Ch 1, which now only points at "VS Code and the CLI" briefly.

### The Databricks extension for VS Code

Runs notebooks on your workspace from a local folder — no manual import.

1. Install the **Databricks** extension (Databricks Inc.) from the Extensions panel.
2. Open a folder → click the Databricks icon → **Create configuration** → pick a workspace (from `~/.databrickscfg`) → select or create compute.

### Two execution modes

- **Interactive (Databricks Connect)** — Spark operations execute on remote Databricks compute; all other code runs locally. Feels identical to a local Jupyter notebook.
    - Works with a classic All-Purpose cluster (**DBR 13.3+**) **or Serverless** (Serverless requires **Databricks Connect 15.4 LTS or above**).
    - Select serverless by setting `serverless_compute_id = "auto"` in the connection config (or the `DATABRICKS_SERVERLESS_COMPUTE_ID` env var) instead of pointing at a `cluster_id`.
    - `spark`, `dbutils`, `display`, and `sql` are pre-injected — no setup code needed.
- **Run as Job** — submits the whole notebook as a Lakeflow Job run (any compute, including Serverless). Open the `.ipynb` → **Run on Databricks → Run File as Workflow**. Results appear in a "Databricks Job Run" tab; the run ID links to full job detail in the workspace UI.

> **Historical note:** early Databricks Connect "v2" (released with DBR 13.3 in 2023) targeted only classic clusters — serverless support arrived in the 15.x line. Notes written before mid-2024 often still claim serverless is unsupported; that restriction no longer applies.

### Why this matters for DevOps

Local IDE development is what makes **unit testing** (pytest against Databricks Connect) and **Git-based workflows** practical — you edit, test, and commit locally, then deploy via DABs (*Ch 20*). The interactive mode gives a fast inner loop; run-as-job validates the real execution path before promotion.

## To write (full chapter)

- pytest / unittest against Databricks Connect; mocking `spark`
- Test pyramid for data pipelines (unit → integration → end-to-end)
- Multi-environment promotion (dev → staging → prod) via DABs targets
- CI gates: validation, tests, and approvals before `prod` deploy
