# Data engineering with Databricks (Lakeflow hub)

> **Source:** [docs.databricks.com/aws/en/data-engineering](https://docs.databricks.com/aws/en/data-engineering/)
> **Added:** 2026-06-25
> **Source updated:** 2026-06-15
> **Tags:** data-engineering, lakeflow, lakeflow-connect, declarative-pipelines, lakeflow-designer, lakeflow-jobs, databricks-runtime, flows, streaming-tables, materialized-views, sinks, B6, I1, I2, I3, I6, A3, A6
> **Type:** documentation

> "Lakeflow is a unified solution for ingestion, transformation, and orchestration of your data, and includes Lakeflow Connect, Lakeflow Spark Declarative Pipelines, Lakeflow Designer, and Lakeflow Jobs."

The hub page for the whole **data engineering** area: data engineering on Databricks **is Lakeflow** — an end-to-end solution for ingestion, transformation, and orchestration, all on top of the **Databricks Runtime for Apache Spark** (with Photon).

- **Lakeflow Connect (ingest)** — connectors to enterprise apps, databases, cloud storage, message buses, and local files. Two tiers: **managed connectors** (config-based UI service, no pipeline-API/infra work) vs **standard connectors** (wider source range from within your own pipelines/queries). → learning path **A3**.
- **Lakeflow SDP (transform)** — declarative framework for batch + streaming pipelines; orchestrates flows, sinks, streaming tables, and materialized views as a **pipeline**. → **I3**.
- **Lakeflow Designer (visual build)** — drag-and-drop canvas + natural-language (Genie Code) prep; every workflow compiles to **production code governed by Unity Catalog**. → I3.
- **Lakeflow Jobs (orchestrate)** — reliable orchestration + monitoring; a job has **tasks** (notebook, pipeline, managed connector, SQL, ML train/deploy/infer) and **control flow** (if/else, for-each). → **I6**.
- **Databricks Runtime for Apache Spark** — the compute substrate (Photon, autoscaling; Spark / Structured Streaming as notebooks, JARs, or wheels). → I2/E2.

DLT rename: "What happened to Delta Live Tables (DLT)?" — DLT is now **Lakeflow Spark Declarative Pipelines**.

## The SDP object model

The hub defines four pipeline objects:

- **Flows** — the unit that *processes* data, using the **same DataFrame API as Apache Spark / Structured Streaming**; a flow writes into streaming tables or sinks (streaming semantics) or a materialized view (batch semantics).
- **Streaming tables** — a Delta table with streaming/incremental support; the **target** for one or more flows.
- **Materialized views** — a view with cached results; a **target** for pipelines ([[materialized-views]]).
- **Sinks** — **external** targets: event-streaming services (Apache Kafka, Azure Event Hubs), UC-managed external tables, or custom Python-defined sinks.

> 💡 Mental model: a **flow** is the verb (it processes/moves data); **streaming tables**, **materialized views**, and **sinks** are the nouns it writes to. SDP wraps a set of flows + targets into one managed **pipeline**.

## How it maps to the learning path

| Lakeflow component | Learning-path topic(s) |
|---|---|
| Lakeflow Connect (managed/standard connectors) | **A3** ingestion; **B6** basics; **I1** Auto Loader |
| Lakeflow SDP (flows, streaming tables, MVs, sinks) | **I3** Declarative Pipelines |
| Lakeflow Designer | **I3** Designer callout |
| Lakeflow Jobs (tasks, control flow) | **I6** Jobs & Orchestration; **A6** ops/observability |
| Databricks Runtime / Spark / Structured Streaming | **I2** Structured Streaming; **E2** advanced streaming |

Related: [[serverless-pipelines]], [[materialized-views]], [[serverless-jobs]], [[procedural-vs-declarative]], [[batch-vs-streaming]].
