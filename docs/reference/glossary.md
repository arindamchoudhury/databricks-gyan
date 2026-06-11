# Glossary

Terms added as they are encountered. Source column shows where the definition came from.

| Term | Definition | Source |
|---|---|---|
| **Lakeflow Spark Declarative Pipelines** | The declarative ETL framework in Databricks (formerly Delta Live Tables / DLT); defines pipelines as SQL or Python table definitions with built-in data quality expectations | Databricks DAIS 2025 |
| **Lakeflow Jobs** | Databricks orchestration system for multi-task workflows (formerly Databricks Workflows / Jobs) | Databricks 2025 |
| **Lakeflow Connect** | Managed ingestion connectors for ingesting from enterprise sources (databases, SaaS) into Databricks | Databricks 2025 |
| **Delta Lake** | Open-source storage format adding ACID transactions, versioning, and schema enforcement to Parquet files | delta.io |
| **Unity Catalog** | Databricks' centralized governance layer providing a three-level namespace (catalog.schema.table), fine-grained ACLs, and data lineage | Databricks docs |
| **Medallion Architecture** | A multi-hop data design pattern: Bronze (raw) → Silver (cleaned, validated) → Gold (business-ready aggregations) | Databricks docs |
| **Auto Loader** | Incremental file ingestion mechanism using cloudFiles source; detects new files in cloud storage using directory listing or file notification | Databricks docs |
| **APPLY CHANGES INTO** | SQL API for processing CDC (Change Data Capture) events into a target Delta table, supporting SCD Type 1 and Type 2 | Databricks docs |
| **Liquid Clustering** | Data layout strategy replacing partitioning and Z-order; dynamically clusters data based on specified columns for optimal skipping | Databricks docs (DBR 14+) |
| **Declarative Automation Bundles (DABs)** | Infrastructure-as-code framework for defining, deploying, and managing Databricks resources (jobs, pipelines, notebooks) as YAML + code. Formerly "Databricks Asset Bundles" — renamed March 2026; CLI commands unchanged. | Databricks docs |
| **OpenSharing** | Open protocol for sharing Delta Lake tables (and Iceberg tables) across organizations and platforms without copying data. Formerly "Delta Sharing" — renamed June 2026; same protocol, new name. opensharing.io | Databricks 2026 |
| **Photon** | Databricks' native vectorized query engine written in C++; accelerates SQL and DataFrame operations | Databricks docs |
| **DBU** | Databricks Unit — the billing unit for compute usage on the platform | Databricks docs |
| **Control Plane / Data Plane** | Control plane: Databricks-managed services (UI, REST API, cluster manager). Data plane: customer's cloud account where compute runs and data lives | Databricks docs |
