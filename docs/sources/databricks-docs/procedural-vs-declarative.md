# Procedural vs. declarative data processing

> **Source:** [docs.databricks.com/aws/en/data-engineering/procedural-vs-declarative](https://docs.databricks.com/aws/en/data-engineering/procedural-vs-declarative)
> **Added:** 2026-06-25
> **Source updated:** 2026-06-15
> **Tags:** data-engineering, concepts, procedural, declarative, lakeflow-jobs, declarative-pipelines, spark, I3, I6
> **Type:** documentation

## Summary

A concepts page explaining the two programming paradigms behind Databricks pipelines. **Procedural** processing says *how*: you write the explicit sequence of steps. **Declarative** processing says *what*: you describe the desired result and let the system pick the execution plan. On Databricks the split is clean — **Apache Spark + Lakeflow Jobs** are the procedural tools; **Lakeflow Spark Declarative Pipelines (SDP)** is the declarative one. The choice drives a pipeline's complexity, maintainability, and how much tuning you do by hand.

## Key points

- **Procedural = imperative, step-by-step.** You define the order of operations and control flow (loops, conditionals, functions). You get fine-grained control and manual performance tuning, at the cost of verbosity and expertise.
- **Declarative = describe the outcome.** The system handles query planning, optimization, and execution tuning. Less control, but simpler and more maintainable.
- **Procedural on Databricks = Apache Spark + Lakeflow Jobs.** Spark primarily follows a procedural model; use Lakeflow Jobs to add explicit step-by-step execution logic. → learning path **I6** (Jobs), **I2** (Spark/Structured Streaming).
- **Declarative on Databricks = Lakeflow SDP.** You specify what to ingest and how to transform; the pipeline automates orchestration, compute management, monitoring, data-quality enforcement, and error handling. → learning path **I3**.

## Notes

### When to choose which

| Choose **procedural** when… | Choose **declarative** when… |
|---|---|
| You need fine-grained control over execution logic. | Simplified development and maintenance are the priority. |
| Transformations involve complex business rules hard to express declaratively. | SQL-based transforms or managed workflows remove the need for procedural control. |
| Performance needs manual tuning. | You want the framework's built-in optimizations (e.g. pipelines). |

Common procedural use cases: custom ETL needing procedural logic; low-level batch/streaming perf tuning; legacy/imperative scripts. Common declarative use cases: SQL transforms in batch/streaming; high-level pipeline frameworks; scalable distributed workloads wanting automatic optimization.

### Paradigm lineage (from the page)

- Procedural is a **sub-class of imperative** programming.
- Declarative includes **domain-specific** and **functional** paradigms.

> 💡 This is the *why* behind I3. The learning path uses "declarative" as a label for SDP; this page is the conceptual contrast that justifies it — SDP trades the hand-control of procedural Spark/Jobs for automatic orchestration and optimization. Reach for procedural (Spark + Jobs) when the logic is too bespoke to express declaratively or you must tune by hand.

## Quotes worth keeping

> "With procedural programming you specify how tasks should be accomplished by defining explicit sequences of operations. Declarative programming focuses on what needs to be achieved, leaving the underlying system to determine the best way to execute the task." (intro)

## Related sources

- [[data-engineering-hub]] — the Lakeflow hub; this page is the concept under the SDP-vs-Jobs split it maps.
- [[serverless-pipelines]] — the declarative engine (SDP) in depth.
- [[materialized-views]] — a declarative pipeline target.
