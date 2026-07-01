# Pipelines (Lakeflow Spark Declarative Pipelines concepts)

> **Source:** [docs.databricks.com — Pipelines](https://docs.databricks.com/aws/en/ldp/concepts/pipelines)
> **Added:** 2026-07-01
> **Source updated:** 2026-06-15
> **Tags:** lakeflow, declarative-pipelines, sdp, pipeline-graph, dag, pipeline-types, lakebase, standalone-pipelines, pipelines-editor, I3, E8
> **Type:** documentation

Breadcrumb: Data engineering › Lakeflow Spark Declarative Pipelines › Concepts › Pipelines. Deepens [[ldp-overview]]'s "concepts" topic entry with the pipeline object itself — the DAG execution model, the four pipeline *types* Databricks actually runs, and the editor.

## What are pipelines?

A **pipeline** is the main unit of development and execution in SDP: a collection of source-code files plus a configuration. Source files declare datasets (streaming tables, materialized views, views) and the queries/flows that produce them. The configuration specifies how the pipeline runs and where data is stored.

The pipeline is the *container* for flows, streaming tables, materialized views, and sinks. While running, it analyzes dependencies between these objects and orchestrates execution order and parallelization automatically.

## Pipeline source code

Written in Python or SQL. A single pipeline can mix both languages, but each individual file is one language only. Because the pipeline analyzes dataset dependencies across *all* source files, files can be organized in any order — you don't have to sequence them yourself.

## Pipeline graph

Pipelines automatically infer dependencies between datasets and arrange them in a **directed acyclic graph (DAG)**. The graph determines evaluation order: upstream datasets compute before downstream ones. The DAG is viewable/interactive in the **Lakeflow Pipelines Editor**.

## Pipeline updates

A pipeline **update** computes the current state of each dataset by:

1. Starting a cluster with the correct configuration.
2. Analyzing source files and building the dependency graph.
3. Computing or incrementally updating each dataset in dependency order.

Pipelines run in two modes:

- **Triggered** — runs once, stops when all datasets are up to date.
- **Continuous** — runs indefinitely, processing new data as it arrives.

Updates triggered interactively from the editor optimize for fast iteration: they reuse the cluster and disable automatic retries.

> This Triggered/Continuous split is the *pipeline-update* trigger mode — distinct from the **serverless trigger modes** (triggered/continuous/real-time) already covered under [[serverless-pipelines]], which govern compute allocation rather than the update-run semantics described here.

## Pipeline types

**New — genuinely absent before this note.** The Jobs & Pipelines list includes more than pipelines created in SDP — Databricks runs several different underlying pipeline mechanisms and labels each with a `pipeline_type` in the event log:

| Type in Jobs & Pipelines | `pipeline_type` in event log | Description |
|---|---|---|
| ETL | `WORKSPACE` | A pipeline defined in Lakeflow SDP. |
| Ingestion | `MANAGED_INGESTION` | A managed ingestion pipeline created with Lakeflow Connect. |
| MV/ST | `DBSQL` | A standalone pipeline (see below). |
| Database Table Sync | `DATABASE_TABLE_SYNC` | A pipeline that syncs a table to a Lakebase database — see "Serve lakehouse data with synced tables (Lakebase Provisioned)". |

> **New Lakebase integration mechanism:** *Database Table Sync* is a distinct path into Lakebase from the one already captured in [[streaming-lakebase]]. The streaming-sink note covers Structured Streaming **writing to** Lakebase via `.toTable()`/JDBC. This `DATABASE_TABLE_SYNC` pipeline type instead **syncs a Lakehouse table into Lakebase** as a managed pipeline — the reverse direction, and a different mechanism (a pipeline, not a streaming query). The linked "synced tables" page wasn't fetched in this pass; flag as a follow-up gap under E8 if pursued further.

## Standalone pipelines

Streaming tables and materialized views can be created/managed **outside** SDP as standalone pipelines, using Databricks SQL or Python. They run on the same infrastructure with the same processing semantics as inside SDP. When you define a standalone streaming table or MV, flows are defined *implicitly* as part of that definition. Confirms [[materialized-views]]'s point that a standalone MV always runs on an auto-created pipeline (type `MV/ST` — same taxonomy entry captured above).

## Lakeflow Pipelines Editor

**New — not previously captured.** An IDE built for pipeline development, providing:

- A multi-file code editor for Python and SQL source files
- A pipeline assets browser for organizing files and folders
- An interactive pipeline graph showing dataset dependencies and state
- Data previews for streaming tables and materialized views
- Execution insights and an issues pane showing results from the latest run
- Selective execution to refresh individual files/tables without running the full pipeline

Integrates with the Databricks platform; supports version control via Git folders.

---
Related: [[ldp-overview]] — the hub this concepts page sits under; [[materialized-views]] — confirms the `MV/ST` pipeline-type detail and standalone-pipeline behavior; [[serverless-pipelines]] — the serverless *trigger-mode* story this note's Triggered/Continuous *update-mode* story is distinct from; [[streaming-lakebase]] — the other (streaming-sink) direction into Lakebase, contrasted with this note's `DATABASE_TABLE_SYNC` pipeline type.
