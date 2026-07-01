# Flows (Lakeflow Spark Declarative Pipelines concepts)

> **Source:** [docs.databricks.com — Load and process data incrementally with Lakeflow Spark Declarative Pipelines flows](https://docs.databricks.com/aws/en/ldp/concepts/flows)
> **Added:** 2026-07-01
> **Source updated:** 2026-06-15
> **Tags:** lakeflow, declarative-pipelines, sdp, flows, append-flow, auto-cdc, update-flow, once-flow, I3
> **Type:** documentation

Breadcrumb: Data engineering › Lakeflow Spark Declarative Pipelines › Concepts › Flows. I3's "What it is" only name-drops **flows** as "the processing unit, same DataFrame API as Spark/Structured Streaming" — this page is the dedicated explanation, including a flow-type taxonomy not previously captured.

## What a flow is

Data is processed in pipelines through **flows**. Each flow consists of a query and, typically, a target. The flow processes the query either as a batch, or incrementally as a stream, into the target. A flow lives *within* a pipeline (see [[ldp-concepts-pipelines]]).

Flows are usually defined **automatically** when you create a query in a pipeline that updates a target — but you can also explicitly define additional flows for more complex processing, e.g. appending to a single target from multiple sources.

## Updates

A flow runs each time its defining pipeline is updated (see [[ldp-concepts-pipelines]]'s Triggered/Continuous update modes). Depending on flow type and the state of source-data changes, an update performs either an **incremental refresh** (only new records) or a **full refresh** (reprocesses everything from source).

## Default flows and append flows

Creating a query in a pipeline that updates a target auto-defines a **default flow**. For a streaming table, the default flow is an **append flow** that adds new rows with each update, named the same as the target. Creating a flow and its target in one step is the most common usage pattern.

You can also define flows **separately** from a target, letting multiple flows append to a single target — useful for:

- Adding streaming sources that append to an existing streaming table without a full refresh.
- Backfilling a streaming table with missing historical data.
- Combining data from multiple sources without a `UNION` clause.

## Types of flows

**New — a flow-type taxonomy absent before this note.**

| Flow type | Description |
|---|---|
| **Append** | The most common type — new source records are written to the target on each update, corresponding to append mode in Structured Streaming. Supports a **`ONCE`** flag: a batch query whose data is inserted into the target only once (unless the target is fully refreshed). Any number of append flows can write to one target. Default flows (created with their target) share the target's name; other targets have no default flow. |
| **Auto CDC** (previously *apply changes*) | Ingests a query containing CDC data — full mechanics already captured in [[what-is-cdc]]. Can **only target streaming tables**, and the source must be a streaming source (even for `ONCE` flows). Multiple Auto CDC flows can target one streaming table, but a streaming table targeted by an Auto CDC flow **can only be targeted by other Auto CDC flows** (no mixing with Append/Update flows on that target). |
| **Update** (Public Preview) | **New — not previously captured.** Outputs global, non-watermarked streaming aggregates to a sink, emitting only the records that changed in each batch. **Python-only** (`update_flow`). |

---
Related: [[ldp-concepts-pipelines]] — the pipeline container this flow taxonomy lives inside, and its Triggered/Continuous update-mode story a flow's own update timing follows; [[what-is-cdc]] — the deep dive on the Auto CDC flow type's mechanics (this page only classifies it); [[data-engineering-hub]] — names flows as one of the four SDP object-model pieces this note now explains in full.
