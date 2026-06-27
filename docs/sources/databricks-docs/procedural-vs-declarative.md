# Procedural vs. declarative data processing

> **Source:** [docs.databricks.com/aws/en/data-engineering/procedural-vs-declarative](https://docs.databricks.com/aws/en/data-engineering/procedural-vs-declarative)
> **Added:** 2026-06-25
> **Source updated:** 2026-06-15
> **Tags:** data-engineering, concepts, procedural, declarative, lakeflow-jobs, declarative-pipelines, spark, I3, I6
> **Type:** documentation

> "With procedural programming you specify how tasks should be accomplished by defining explicit sequences of operations. Declarative programming focuses on what needs to be achieved, leaving the underlying system to determine the best way to execute the task."

A concepts page on the two paradigms behind Databricks pipelines. **Procedural** says *how* — you write the explicit sequence of steps and control flow (loops, conditionals, functions), getting fine-grained control and manual tuning at the cost of verbosity and expertise. **Declarative** says *what* — you describe the desired result and the system handles query planning, optimization, and execution tuning (less control, simpler, more maintainable). On Databricks the split is clean: **Apache Spark + Lakeflow Jobs** are the procedural tools (→ learning path I6/I2); **Lakeflow Spark Declarative Pipelines (SDP)** is the declarative one (→ I3). Paradigm lineage: procedural is a sub-class of imperative; declarative includes domain-specific and functional paradigms.

## When to choose which

| Choose **procedural** when… | Choose **declarative** when… |
|---|---|
| You need fine-grained control over execution logic. | Simplified development and maintenance are the priority. |
| Transformations involve complex business rules hard to express declaratively. | SQL-based transforms or managed workflows remove the need for procedural control. |
| Performance needs manual tuning. | You want the framework's built-in optimizations (e.g. pipelines). |

Common procedural use cases: custom ETL needing procedural logic; low-level batch/streaming perf tuning; legacy/imperative scripts. Common declarative use cases: SQL transforms in batch/streaming; high-level pipeline frameworks; scalable distributed workloads wanting automatic optimization.

> 💡 This is the *why* behind I3: SDP trades the hand-control of procedural Spark/Jobs for automatic orchestration and optimization. Reach for procedural (Spark + Jobs) when the logic is too bespoke to express declaratively or you must tune by hand.

Related: [[data-engineering-hub]], [[serverless-pipelines]], [[materialized-views]], [[batch-vs-streaming]].
