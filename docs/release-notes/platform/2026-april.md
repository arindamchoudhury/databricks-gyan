# Platform Release Notes — April 2026

> **Source:** [docs.databricks.com/aws/en/release-notes/product/2026/april](https://docs.databricks.com/aws/en/release-notes/product/2026/april)
> **Added:** 2026-06-11

---

## Data Engineering highlights

### Lakeflow Jobs

**Task disable (GA)** — April 30
Skip tasks at runtime without removing them. Disabled tasks retain config and history.

### Lakeflow Spark Declarative Pipelines

**Pipeline update history retention extended: 30 → 60 days** — April 28

**`cascade` field for pipeline deletion (Beta)** — April 9
`DELETE /pipelines/{id}?cascade=false` preserves associated UC tables when deleting a pipeline.

**Lakeflow Designer (Public Preview)** — April 22
Drag-and-drop canvas with natural language for building transformation workflows.

### Unity Catalog & Governance

**ABAC (GA) — Breaking change** — April 28
Attribute-Based Access Control policies now evaluate using the **session user's identity** (not view/function owner). Three-month grace period for affected customers.
> ⚠️ **Breaking change:** Review existing row filters and column masks — owner-based evaluation changes to session-user evaluation.

**Governed Tags (GA)** — April 2
Admins define a controlled tag set applicable to UC and workspace objects.

**Customer-managed keys for Unity Catalog (GA)** — April 1
Encrypt catalog data with your own cloud KMS keys.

**Tag UC Functions** — April 28
Functions are now taggable securable objects (`SET TAG`, `UNSET TAG`).

**Column-level SAP governance tags** — April 13
Governance tags from SAP Business Data Cloud sync into UC for ABAC policies.

### Lakeflow Connect

**Query-based connectors (Public Preview)** — April 15
Direct cursor query ingestion from Oracle, Teradata, SQL Server, MySQL, MariaDB, PostgreSQL, and Lakehouse Federation — no CDC required.

**Zendesk Support connector (GA)** — April 28

**Cloud token access for Delta Sharing (GA)** — April 28
Recipients read shared tables directly from cloud storage without pre-signed URLs.

**Share foreign Iceberg tables (Public Preview)** — April 9
Delta Sharing now supports sharing read-only foreign Iceberg tables from federated catalogs.

### Compute

**DBR 18.2 (Beta)** — Apache Spark 4.1.0.
**Compute log delivery to Volumes (GA)** — April 16
Deliver Spark driver, worker, and event logs to UC Volumes (recommended over DBFS).

### SQL

**`ai_parse_document` (GA)** — April 16
Parse structured content from PDFs, images, Word docs, PowerPoint (max 500 pages, 100 MB).

**5X-Large SQL Warehouse (Public Preview)** — April 28
512-worker option for serverless and pro SQL warehouses.
