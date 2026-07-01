# Lakeflow Spark Declarative Pipelines

> **Source:** [docs.databricks.com — Lakeflow Spark Declarative Pipelines](https://docs.databricks.com/aws/en/ldp/)
> **Added:** 2026-07-01
> **Source updated:** 2026-06-15
> **Tags:** lakeflow, declarative-pipelines, sdp, data-engineering, hub, I3
> **Type:** documentation

Breadcrumb: Data engineering › Lakeflow Spark Declarative Pipelines. This is the top-level hub page for the pipelines framework — thin by design, it's a topic directory rather than reference content.

> 📌 **URL rename:** this hub moved from `docs.databricks.com/aws/en/dlt/` to `docs.databricks.com/aws/en/ldp/` (the old `/dlt/` path 301-redirects to `/ldp/`, confirmed same content). Sub-pages follow the same pattern (`/dlt/cdc.html` → `/ldp/cdc.html`, `/dlt/observability.html` → `/ldp/observability.html`). The three bare `/dlt/...` links already in [[learning-path]] I3 still resolve via redirect but should be updated to `/ldp/...` going forward.

Lakeflow Spark Declarative Pipelines (SDP) is a framework for creating batch and streaming data pipelines in SQL and Python. It runs on the performance-optimized Databricks Runtime.

> **New detail — Apache Spark Declarative Pipelines:** Lakeflow SDP "extends and is interoperable with **Apache Spark Declarative Pipelines**" — an open-source declarative-pipelines project now in upstream Apache Spark. Not previously named in the path; SDP is Databricks' Runtime-optimized superset of it, not a Databricks-only proprietary framework.

Common use cases named: data ingestion from cloud storage (S3, ADLS Gen2, GCS) and message buses (Kafka, Kinesis, Google Pub/Sub, Azure EventHub, Pulsar), and incremental batch/streaming transformations.

## Topics on this hub

| Topic | Description |
|---|---|
| Lakeflow Spark Declarative Pipelines concepts | High-level concepts of SDP: pipelines, flows, streaming tables, and materialized views |
| Tutorials | Hands-on tutorials for using pipelines |
| Develop pipelines | Develop and test pipelines that create flows for ingesting and transforming data |
| Configure pipelines | Schedule and configure pipelines |
| Monitor pipelines | Monitor pipelines and troubleshoot pipeline queries |
| Developers | Using Python and SQL when developing pipelines |
| Standalone pipelines | Creating standalone streaming tables and materialized views in Databricks SQL or Python |
| Best practices | Recommended patterns for reliable, efficient, maintainable pipelines |

**Additional resources** linked from this hub: Pipeline limitations, Pipeline developer reference (not separately captured here).

---
Related: [[data-engineering-hub]] — the broader Lakeflow umbrella this pipelines hub sits under; [[procedural-vs-declarative]] — the paradigm this framework embodies; [[materialized-views]] and [[serverless-pipelines]] — deeper dives into two of this hub's own subtopics, already captured.
