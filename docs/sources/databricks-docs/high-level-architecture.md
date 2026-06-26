# High-level architecture

> **Source:** [docs.databricks.com/gcp/en/getting-started/high-level-architecture](https://docs.databricks.com/gcp/en/getting-started/high-level-architecture)
> **Added:** 2026-06-20
> **Source updated:** 2026-03-16
> **Tags:** architecture, control-plane, compute-plane, account, workspace, unity-catalog, serverless, classic, workspace-storage, gcp, B1
> **Type:** documentation

Databricks runs as a **control plane** (Databricks-managed backend services and the web app, in the Databricks account) plus a **compute plane** (where data is processed — either serverless, in the Databricks account, or classic, in your own cloud account). Above workspaces sits the **account**, the top-level construct for identity, workspace, and Unity Catalog metastore management. Each workspace also keeps its own **workspace storage** (file-system data + system data), separate from your actual data objects. This is the GCP edition of the page; the split is the same on every cloud, only the bucket terminology is cloud-specific.

## Databricks objects — the account hierarchy

[![Databricks object hierarchy](assets/high-level-architecture/01-object-hierarchy.png)](assets/high-level-architecture/01-object-hierarchy.png)
*Account is the top-level construct; it contains workspaces and Unity Catalog metastores.*

A **Databricks account** is the top-level construct for managing Databricks org-wide. At the account level you manage **identity and access** (users, groups, service principals, SCIM, SSO), **workspace management** (create/update/delete across regions), **Unity Catalog metastore management**, and **usage** (billing, compliance, policies). One account can contain **multiple workspaces and multiple metastores**.

**Workspaces** are the collaboration environment where users run compute workloads — ingestion, interactive exploration, scheduled jobs, ML training. **Unity Catalog metastores** are the central governance system for data assets, organized under the three-level namespace `<catalog>.<schema>.<object>`; a single metastore can link to multiple workspaces **in the same region**, giving each the same data view with shared access controls.

## Workspace architecture — control plane vs compute plane

> "The control plane is located in the Databricks account, not your cloud account. The web application is in the control plane."

- **Control plane** — backend services Databricks manages, in the **Databricks account**; the web app lives here.
- **Compute plane** — where data is processed. **Serverless** runs in a serverless compute plane in the **Databricks account**; **classic** runs in **your Google Cloud resources** (each workspace's virtual network).

This is the platform-level distinction behind [[classic-compute-overview]] (your cloud account) vs [[serverless-notebooks]] / [[serverless-limitations]] (Databricks-managed infrastructure).

## Classic workspace architecture

[![Databricks classic architecture for GCP](assets/high-level-architecture/02-classic-architecture-gcp.png)](assets/high-level-architecture/02-classic-architecture-gcp.png)
*Compute runs in the customer's GCP project.*

Classic workspaces have **three associated storage buckets** in your Google Cloud account.

## Serverless workspace architecture

[![Databricks serverless workspace architecture](assets/high-level-architecture/03-serverless-architecture.png)](assets/high-level-architecture/03-serverless-architecture.png)
*Workspace storage lives in default storage.*

Workspace storage in serverless workspaces is in the workspace's **default storage**. You can also connect to your own cloud storage to access your data.

## Compute planes

**Serverless compute plane** — runs in a compute layer **within your Databricks account**, in the **same GCP region** as the workspace's classic plane. To protect data, serverless compute runs within a **network boundary for the workspace**, with multiple security layers isolating workspaces plus controls between clusters of the same customer.

**Classic compute plane** — runs in **your Google Cloud account**, within each workspace's **virtual network**, giving **natural isolation** because it's your own account.

## Workspace storage

Workspace storage holds **two categories of data**, both separate from your own data objects (UC tables and volumes):

- **Workspace file system data** — assets users create through the UI: notebooks, SQL queries and dashboards, alerts, repos, libraries (`.whl`, `.jar`), Python/YAML and other small files.
- **Workspace system data** — generated internally: SQL query results + cached results, job run results, notebook revisions, query plans (observability), cluster logs.

**Serverless workspaces** use **default storage** — a fully managed location for internal system data **and** UC data assets; you can also connect your own cloud storage for catalogs/tables.

**Classic workspaces** get **three buckets** in your GCP account: (1) **system data bucket** (internal Databricks data); (2) **DBFS root bucket** (legacy, may be disabled — storing/accessing data via DBFS root or mounts is a **deprecated** pattern); (3) **default UC workspace catalog bucket** (only if auto-enabled for UC). Workspace system data is distinct from DBFS even when they share buckets.

> ⚠️ **Do not delete or modify classic workspace storage.** A workspace depends on both its control-plane databases and its workspace storage. "If workspace storage is deleted, the workspace cannot be recovered."

Related: [[classic-compute-overview]], [[serverless-limitations]], [[dedicated-compute-overview]], [[standard-compute-overview]], [[lakehouse-what-is]].
