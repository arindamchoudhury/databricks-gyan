# DCDE-SG Ch 1 — verified facts

Last verified: **2026-06-14** against Databricks platform docs + the 2026 DCDEA exam guide.

Working file for note-taking on Derar Alhussein's *Databricks Certified Data Engineer Associate Study Guide* (O'Reilly, 1st Ed., Feb 2025). The book targets the older exam aligned to **DBR 13.3 LTS** and references **Community Edition**; these facts capture what changed by mid-2026.

| Book claim (2025) | Current value (2026) | Notes |
|---|---|---|
| Cluster access modes: "Shared" / "Single user" | **Standard** (was Shared) / **Dedicated** (was Single user) | Dedicated now also assignable to a group, and supports ML runtime, RDD APIs, R, Scala that Standard restricts. |
| Recommended runtime: **DBR 13.3 LTS** (exam alignment) | Current: **DBR 18** (Spark 4.1.0) / **DBR 17.3 LTS** (Spark 4.0.0) | Book pins 13.3 because the *then-current* exam aligned to it. New DCDEA exam version goes live **May 4, 2026**. |
| **Community Edition** for free/training use | **Retired Jan 1, 2026** → **Databricks Free Edition** (perpetual, serverless, no cloud account) | Sign up at `login.databricks.com`; URL `https://<ws>.cloud.databricks.com`. Free Edition runs on AWS. |
| DBC import needed because CE lacks Git folders | On Free Edition, Git folders **are** available (UC-enabled) | The book's "Option 2: DBC files (Community Edition)" path is now mostly historical. |
| DBFS used freely for storage | **DBFS root & mounts deprecated**; new workspaces are **Unity Catalog-only** (Azure: all new workspaces UC-only from **Sep 30, 2026**) | `/databricks-datasets` still accessible read-only. UC **Volumes** (`/Volumes/cat/schema/vol/`) are the replacement for user data. `dbfs:/Volumes` scheme still works. |
| "Delta Live Tables (DLT) pipelines" (Ch 6 forward-ref) | **Lakeflow Spark Declarative Pipelines** (renamed DAIS 2025) | Same declarative ETL framework. |
| 14-day free trial on your cloud | Still offered; **Free Edition** is the no-cost perpetual alternative | |

## 2026 DCDEA exam quick facts

- 45 scored multiple-choice questions, 90 minutes, USD 200, valid 2 years.
- New exam version live **May 4, 2026**. Five domains: Databricks Intelligence Platform (10%), Development & Ingestion (30%), Data Processing & Transformations (31%), Productionizing Data Pipelines (18%), Data Governance & Quality (11%).

## Sources

- Cluster access modes: <https://docs.databricks.com/aws/en/compute/configure>
- 2026 exam guide: <https://www.databricks.com/sites/default/files/2026-03/databricks-certified-data-engineer-associate-exam-guide-may-4-2026.pdf>
- DBFS/UC best practices: <https://docs.databricks.com/aws/en/dbfs/unity-catalog>
- UC Volumes: <https://docs.databricks.com/aws/en/volumes/>
