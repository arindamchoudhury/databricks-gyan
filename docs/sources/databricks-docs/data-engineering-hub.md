# Data engineering with Databricks (Lakeflow hub)

> **Source:** [docs.databricks.com/aws/en/data-engineering](https://docs.databricks.com/aws/en/data-engineering/)
> **Added:** 2026-06-25
> **Source updated:** 2026-06-15
> **Tags:** data-engineering, lakeflow, lakeflow-connect, declarative-pipelines, lakeflow-designer, lakeflow-jobs, databricks-runtime, flows, streaming-tables, materialized-views, sinks, B6, I1, I2, I3, I6, A3, A6
> **Type:** documentation

## Summary

The hub page for the whole **data engineering** area. Its single framing idea: data engineering on Databricks is **Lakeflow**, an end-to-end solution for **ingestion, transformation, and orchestration**. Lakeflow has four named components — **Lakeflow Connect** (ingest), **Lakeflow Spark Declarative Pipelines / SDP** (transform), **Lakeflow Designer** (visual/no-code build), and **Lakeflow Jobs** (orchestrate) — all sitting on top of the **Databricks Runtime for Apache Spark** (with Photon). This page is the index that ties together the learning path's ingestion (B6, I1, A3), streaming (I2, E2), pipelines (I3), and orchestration (I6, A6) topics.

## Key points

- **Lakeflow = the umbrella brand** for Databricks data engineering: Connect + SDP + Designer + Jobs, on the Databricks Runtime.
- **Lakeflow Connect (ingest):** connectors to enterprise apps, databases, cloud storage, message buses, and local files. Two tiers — **managed connectors** (config-based UI service, no pipeline-API/infra work) vs **standard connectors** (access a wider range of sources from within your own pipelines/queries). → learning path **A3**.
- **Lakeflow SDP (transform):** declarative framework for batch + streaming pipelines; extends/interoperates with Apache Spark Declarative Pipelines; runs on the perf-optimized Databricks Runtime. It orchestrates **flows, sinks, streaming tables, and materialized views** by running them as a **pipeline**. → learning path **I3**.
- **Lakeflow Designer (visual build):** drag-and-drop canvas + natural-language (Genie Code) data prep; every workflow compiles to **production code governed by Unity Catalog**. → I3 callout.
- **Lakeflow Jobs (orchestrate):** reliable orchestration + production monitoring for any data/AI workload; a job has **tasks** (notebook, pipeline, managed connector, SQL, ML train/deploy/infer) and **control flow** (if/else branching, for-each looping). → learning path **I6**.
- **Databricks Runtime for Apache Spark:** the compute substrate — Photon vectorized engine, autoscaling; run Spark / Structured Streaming as notebooks, JARs, or Python wheels. → Spark/streaming topics (I2, E2).
- **DLT rename:** "What happened to Delta Live Tables (DLT)?" — DLT is now **Lakeflow Spark Declarative Pipelines**. (Already tracked in I3.)

## Notes

### The SDP object model (the part the learning path under-names)

The hub defines four pipeline objects. Streaming tables and materialized views were already in I3; **flows** and **sinks** were not:

- **Flows** — the unit that *processes* data in a pipeline. Uses the **same DataFrame API as Apache Spark / Structured Streaming**. A flow can write into **streaming tables** or **sinks** (streaming semantics) or into a **materialized view** (batch semantics).
- **Streaming tables** — a **Delta table with streaming/incremental support**; acts as the **target** for one or more flows.
- **Materialized views** — a view with cached results for faster access; acts as a **target** for pipelines (see [[materialized-views]]).
- **Sinks** — **external** pipeline targets: event-streaming services (**Apache Kafka**, **Azure Event Hubs**), **external tables** managed by Unity Catalog, or **custom Python-defined** sinks.

> 💡 Mental model: a **flow** is the verb (it processes/moves data); **streaming tables**, **materialized views**, and **sinks** are the nouns it writes to. SDP wraps a set of flows + targets into one managed **pipeline**.

### How it maps to the learning path

| Lakeflow component | Learning-path topic(s) |
|---|---|
| Lakeflow Connect (managed/standard connectors) | **A3** — Lakeflow Connect & Enterprise Ingestion; **B6** ingestion basics; **I1** Auto Loader |
| Lakeflow SDP (flows, streaming tables, MVs, sinks) | **I3** — Lakeflow Spark Declarative Pipelines |
| Lakeflow Designer | **I3** 🆕 Designer callout |
| Lakeflow Jobs (tasks, control flow) | **I6** — Lakeflow Jobs & Orchestration; **A6** ops/observability |
| Databricks Runtime / Spark / Structured Streaming | **I2** Structured Streaming; **E2** advanced streaming |

## Quotes worth keeping

> "Lakeflow is a unified solution for ingestion, transformation, and orchestration of your data, and includes Lakeflow Connect, Lakeflow Spark Declarative Pipelines, Lakeflow Designer, and Lakeflow Jobs." (intro)

## Related sources

- [[serverless-pipelines]] — serverless compute for SDP pipelines (the engine flows run on).
- [[materialized-views]] — the MV pipeline target, in depth (standalone + serverless).
- [[serverless-jobs]] — serverless compute for Lakeflow Jobs.
