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
| **`read_files()`** | SQL table-valued function for reading files from a Volume or path with inline format options (format, header, inferSchema). Automatically adds a `_rescued_data` column for rows that don't match the inferred schema. | DA-FREE M2-01 |
| **COPY INTO** | Idempotent, incremental SQL command for batch file ingestion into a Delta table. Tracks loaded file paths in the Delta log so re-runs load only new files. | DA-FREE M2-02 |
| **CTAS (CREATE TABLE AS SELECT)** | DDL pattern that creates a Delta table and populates it in one atomic statement. Used for one-shot full loads or Silver layer full refreshes. | DA-FREE M2-01 |
| **`CREATE OR REPLACE TABLE AS SELECT` (CRAS)** | CTAS variant that atomically drops and re-creates the table on each run. Resets Delta history. Common for Silver layer full refreshes. | DA-FREE M2-03 |
| **`INSERT OVERWRITE`** | Replaces all rows in a Delta table while keeping the table definition, properties, and version history. Adds a new Delta version on each run. Common for Gold layer refreshes. | DA-FREE M2-03 |
| **Managed table** | A table whose data lifecycle is owned by Unity Catalog. `DROP TABLE` removes both the catalog entry and the underlying files. Default for `CREATE TABLE` without `LOCATION`. | DA-FREE M2-01 |
| **External table** | A table that points to user-managed cloud storage (`LOCATION` clause). `DROP TABLE` removes the catalog entry but not the data files. | DA-FREE M2-01 |
| **Time travel** | Querying a past version of a Delta table via `VERSION AS OF n`, `@vN`, or `TIMESTAMP AS OF`. Requires old files not to have been vacuumed. | DA-FREE M2-01 |
| **`DESCRIBE DETAIL`** | SQL command that returns storage metadata for a Delta table: format, location, numFiles, sizeInBytes, partitionColumns. | DA-FREE M2-01 |
| **`DESCRIBE HISTORY`** | SQL command that returns the full version history of a Delta table: version number, timestamp, operation, operationMetrics. | DA-FREE M2-01 |
| **`IDENTIFIER` clause** | SQL clause that interprets a string expression as a named object (catalog, schema, table). Used with variables: `USE SCHEMA IDENTIFIER(DA.schema_name)`. | DA-FREE M2-01 |
| **Temp view** | A session-scoped view created with `CREATE [OR REPLACE] TEMP VIEW`. Not persisted to the Unity Catalog; disappears when the session ends. | DA-FREE M2-03 |
| **`_rescued_data`** | Column automatically added by `read_files()` to capture rows where a value couldn't be parsed into the inferred schema type. Non-null values indicate data quality issues. | DA-FREE M2-01 |
| **`_metadata`** | Struct column available on file-based DataFrames containing file-level metadata: `file_name`, `file_path`, `file_size`, `file_modification_time`. Replaces removed `input_file_name()` function (DBR 17.3+). | DA-FREE M2-02 |
| **Git folders** | Workspace folders connected to a Git provider (GitHub, GitLab, Bitbucket). Replaces the legacy Repos feature. Credentials configured in Settings → Developer → Linked Accounts. | DA-FREE M1 |
| **MWS (Multi-Workspace Storage)** | The Databricks account-level API tier for provisioning workspaces and configuring cloud infrastructure. All `databricks_mws_*` Terraform resources target the MWS endpoint (`accounts.cloud.databricks.com`). | Ch 29 — E7 |
| **`databricks_mws_workspaces`** | Terraform resource that creates a Databricks workspace on AWS or GCP by combining credentials, storage configuration, and network configuration. | Ch 29 — E7 |
| **`databricks_grants`** | Authoritative Terraform resource for Unity Catalog permissions — replaces *all* existing grants on a securable when applied. Use `databricks_grant` (per-principal) when other teams manage other principals. | Ch 29 — E7 |
| **Terragrunt** | Open-source wrapper around Terraform (by Gruntwork) that eliminates DRY violations: manages remote state backends, generates provider configurations, and orchestrates multi-unit deployments with dependency ordering. | Ch 29 — E7 |
| **Terragrunt unit** | A single Terraform root module with a `terragrunt.hcl` configuration file. The basic deployable entity in Terragrunt. Each unit has its own isolated state file. | Ch 29 — E7 |
| **Terragrunt stack** | A set of Terragrunt units defined in a `terragrunt.stack.hcl` file. `terragrunt run --all apply` deploys all units in dependency order, with optional parallelism. | Ch 29 — E7 |
| **Cross-account IAM role** | An AWS IAM role that Databricks assumes to create and manage resources (EC2 instances, security groups, ENIs) in the customer's VPC. Required for all AWS workspace deployments. | Ch 29 — E7 |
| **`time_sleep` (Terraform)** | Terraform resource from the `hashicorp/time` provider that introduces a deliberate wait between resource operations. Used after IAM policy attachment to absorb AWS propagation delay before Databricks validates the cross-account role. | Ch 29 — E7 |
| **Security Reference Architecture (SRA)** | Databricks' official opinionated Terraform template for a hardened production workspace deployment: Private Link VPC endpoints, customer-managed KMS keys, restrictive VPC endpoint policies, disabled legacy DBFS/access settings, audit log delivery, and the Security Analysis Tool. Available at `terraform-databricks-sra`. | Ch 29 — E7 |
| **Network Connectivity Configuration (NCC)** | Account-level Databricks object that controls network egress rules for serverless compute (SQL Warehouses, serverless jobs). Required for Private Link on serverless; without it, serverless clusters use Databricks-managed networking. | Ch 29 — E7 |
| **Security Analysis Tool (SAT)** | Databricks workflow that runs automated security posture checks against a workspace and produces a SQL dashboard scoring configuration across network security, identity, data protection, and governance. Deployed as part of the SRA. | Ch 29 — E7 |
| **Customer-Managed Keys (CMK)** | AWS KMS keys provided by the customer to encrypt Databricks data at rest. The SRA creates two: one for workspace storage (DBFS root + EBS volumes) and one for managed services (control-plane data: notebooks, secrets, query results). | Ch 29 — E7 |
