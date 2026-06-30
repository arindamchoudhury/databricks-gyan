# Declarative Automation Bundles (DABs) — Release Notes

> **Source:** [docs.databricks.com/aws/en/release-notes/dev-tools/bundles](https://docs.databricks.com/aws/en/release-notes/dev-tools/bundles)
> **Added:** 2026-06-11
> **Note:** Formerly "Databricks Asset Bundles" — renamed "Declarative Automation Bundles" in March 2026. CLI commands (`databricks bundle`) unchanged.

---

## 2026

**Direct deployment engine (GA)** — June 10, 2026 (CLI 1.3.0)
New bundles created with CLI 1.3.0+ use the direct deployment engine by default instead of Terraform. See Migrate to the direct deployment engine.
> **Learning path note (A5):** The Terraform-free engine (Preview since Dec 2025) is now GA and the default for new bundles.

**Genie space resource** — June 10, 2026 (CLI 1.3.0)
`genie_space` resource — define Genie spaces in bundle configuration.

**Selective deployment — `--select` option** (June 4, 2026)
`databricks bundle plan --select <resource>` and `databricks bundle deploy --select <resource>` — deploy specific resources without deploying the whole bundle.

**Vector Search resources** (May 27, 2026)
`vector_search_endpoint` and `vector_search_index` resources supported (CLI 1.1.0).

**YAML auto-update** (May 2026)
UI edits to jobs and pipeline settings automatically update bundle YAML.

---

## 2025

**Python support (GA)** — October 27, 2025 (CLI 0.275.0)
Define resources in Python and modify resources during deployment. Previously YAML-only.

**Bundles in workspace (GA)** — October 15, 2025
Collaborative bundle editing in Databricks UI — edit, commit, test, deploy through the UI.

**Direct deployment engine** — December 4, 2025 (CLI 0.279.0)
`databricks bundle migrate` removes Terraform dependency. Migration toward a native deployment system.
> **Learning path note (A5):** No longer need Terraform for DABs deployment — the CLI handles it natively.

**SQL alerts resource** — December 4, 2025 (CLI 0.279.0)

**Minimal template** — November 13, 2025 (CLI 0.277.0)
Lightweight starting point alongside the default template.

**Lakeflow Spark Declarative Pipelines template updates** — November 5, 2025
Template updated for current naming conventions.

**Python template with `uv` and `pyproject.toml`** — July 2, 2025
Modernized Python project structure.

**Bundle scripts** — July 16, 2025
Configure and run authenticated scripts as part of bundle lifecycle.

**Dynamic artifact versioning** — June 18, 2025 (new `artifacts_dynamic_version` preset)
Automatic wheel version updates on each deploy.

**Bind/Unbind extended to all resource types** — March–April 2025
Clusters, dashboards, registered models, volumes, quality monitors, model serving endpoints.

**Lakebase resources** — August 2025 (CLI 0.265.0)
Database instances and catalogs.

---

## 2024

**Apps management** — January 16, 2025 (CLI 0.239.0)

**Unity Catalog volumes** — December 5, 2024 (CLI 0.236.0)

**AI/BI dashboards** — October 30, 2024 (CLI 0.232.0)

**All-purpose clusters** — October 1, 2024 (CLI 0.229.0)

**Workspace path prefixing** — October 9, 2024
Paths automatically prefixed with `/Workspace` for consistency with UC Volumes paths.

**Pipeline `run_as`** — September 3, 2025
Identity management for pipeline execution.

---

## Key patterns

```yaml
# databricks.yml
bundle:
  name: my-pipeline-bundle

variables:
  cluster_size:
    default: "Small"
    description: "Cluster size for job cluster"

targets:
  dev:
    mode: development
    variables:
      cluster_size: "Small"
  prod:
    mode: production
    variables:
      cluster_size: "Large"

resources:
  jobs:
    my_etl_job:
      name: "My ETL Job"
      tasks:
        - task_key: ingest
          notebook_task:
            notebook_path: ./notebooks/ingest.py
```

```bash
# CLI commands
databricks bundle validate
databricks bundle deploy --target dev
databricks bundle deploy --target prod
databricks bundle deploy --select resources.jobs.my_etl_job   # selective (2026)
databricks bundle run my_etl_job
databricks bundle migrate   # remove Terraform dependency (2025)
```
