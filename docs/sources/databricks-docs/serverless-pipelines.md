# Serverless compute for Lakeflow Spark Declarative Pipelines

> **Source:** [docs.databricks.com/aws/en/ldp/serverless](https://docs.databricks.com/aws/en/ldp/serverless)
> **Added:** 2026-06-16
> **Source updated:** 2026-06-15
> **Tags:** serverless, pipelines, lakeflow, ldp, dlt, compute, performance-modes, I5
> **Type:** documentation

## Summary

Serverless pipelines run Lakeflow Spark Declarative Pipelines (formerly Delta Live Tables) on Databricks-managed infrastructure — no cluster configuration needed. Unity Catalog is required; any existing cluster config is removed when serverless is enabled. Two performance modes (Standard vs Performance Optimized) mirror the same pattern in [[serverless-jobs]]. Some workloads require classic compute or the legacy Hive metastore and cannot use serverless.

## Key points

- **Prerequisite:** Unity Catalog enabled workspace; no cluster creation permission required.
- Databricks recommends serverless for all **new** pipeline development. Exception: some workloads require classic compute or the legacy Hive metastore.
- **Existing cluster config is wiped** when serverless is enabled — cannot add compute via `clusters` in JSON.
- Two performance modes for triggered pipelines: **Standard** (lower DBU, 4–6 min startup) and **Performance Optimized** (faster, higher DBU).
- Three exclusive serverless features: **incremental refresh** (with full-refresh fallback), **stream pipelining** (concurrent microbatches, on by default), **vertical autoscaling** (adds to horizontal autoscaling).
- AWS PrivateLink requires contacting Databricks.

## Notes

### Requirements

- Workspace must have **Unity Catalog enabled** — same as [[serverless-notebooks]] and [[serverless-jobs]].
- User must accept serverless terms of use.
- Workspace location must be in a supported serverless compute region.
- **No cluster creation permission needed** — all workspace users can configure serverless pipelines by default.

### Configuration options

Serverless pipelines support these settings:

- **Pipeline mode** — Continuous (for production) or Triggered.
- **Notifications** — email alerts on pipeline success/failure.
- **Configuration field** — key-value pairs; referenceable in source code and usable for Spark configuration.
- **Preview channel** — test against pending runtime changes before they reach GA.
- **Environment settings** — declare external Python dependencies.
  - ⚠️ `dbutils.library.restartPython()` is **not supported** in serverless pipelines.
- **Serverless usage policy** *(Public Preview)* — apply custom tags for billing attribution. Existing pipelines must be manually updated to inherit a new policy.

### Converting an existing pipeline to serverless

1. **Jobs & Pipelines** in sidebar → click the pipeline name.
2. Click **Settings**.
3. Under **Compute**, click the pencil icon.
4. Check **Serverless**.
5. Click **Save**.

> ⚠️ "When you enable serverless, any compute settings you have configured for a pipeline are removed." Any `clusters` config in the pipeline JSON is discarded.

### Performance modes (triggered pipelines only)

Identical SKU for both modes; difference is startup latency and DBU consumption:

| Mode | Startup | DBU use | Best for |
|---|---|---|---|
| **Standard** | 4–6 min | Lower | Cost-sensitive, latency-tolerant pipelines |
| **Performance Optimized** | Fast | Higher | Time-sensitive, SLA-bound pipelines |

> 💡 Same two modes as [[serverless-jobs]] — identical names, identical trade-off, same SKU. Continuous pipelines don't have a startup-latency concern, so mode selection is more relevant for triggered pipelines.

### Serverless-exclusive features

Three capabilities only available on serverless pipelines (not classic clusters):

- **Incremental refresh** — materialized views are refreshed incrementally whenever possible. Falls back to a full refresh if results cannot be computed incrementally.
- **Stream pipelining** — microbatches run concurrently instead of sequentially (standard Spark Structured Streaming runs them sequentially), improving compute resource utilisation. Enabled by default on serverless pipelines.
- **Vertical autoscaling** — *adds to* the horizontal autoscaling provided by Databricks enhanced autoscaling by automatically allocating the most cost-efficient instance types that can run the pipeline without out-of-memory errors.

### Monitoring costs

Query the **billable usage system table** to track serverless pipeline DBU consumption. Same approach as [[serverless-jobs]].

## Open questions

- ❓ Can Performance Optimized mode be set for continuous pipelines, or only triggered?
- ❓ What Python dependency installation mechanism is supported if `restartPython()` is unavailable? (Page links to environment settings but doesn't detail it.)
- ❓ Which regions support serverless compute for pipelines?

## Related sources

- [[serverless-jobs]] — same Standard/Performance Optimized mode split, same UC requirement, same billable-usage tracking pattern. Key difference: jobs support 5 task types; pipelines are pipeline-only.
- [[serverless-notebooks]] — same UC prerequisite, no cluster config needed, query insights replace Spark UI.
- [[ch01-getting-started-with-databricks]] — DCDE-SG Ch 1 briefly covers DLT/Lakeflow Pipelines as a product area; serverless is the recommended compute path for new pipelines.
