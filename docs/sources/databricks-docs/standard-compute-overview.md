# Standard compute overview

> **Source:** [docs.databricks.com/aws/en/compute/standard-overview](https://docs.databricks.com/aws/en/compute/standard-overview)
> **Added:** 2026-06-16
> **Source updated:** 2025-10-07
> **Tags:** compute, classic-compute, access-modes, standard, lakeguard, multi-user, B1
> **Type:** documentation

> "Standard compute is compute configured with standard access mode. Standard compute resources can be used by any user given permission to do so."

Standard is the **multi-user shared** access mode — any number of permissioned users can attach and concurrently execute workloads on the same resource, for cost savings and simpler compute management (contrast Dedicated, which is single-user or group-assigned). It's **recommended for most workloads** and secured by **Databricks Lakeguard**. Use **Dedicated instead** when you need RDD APIs, distributed ML requiring privileged machine access, GPUs, or **R** (R is not supported on standard; Scala needs DBR 13.3 LTS+ with Unity Catalog).

## Access mode selection

Configured in the **Advanced** section of the compute creation UI; the API field is `data_security_mode`. Default is **Auto**: resolves to **Standard** unless an ML runtime or DBR < 14.3 is selected (then **Dedicated**). See [[classic-compute-configure]] for full config and [[classic-compute-overview]] for permission levels.

## When to use standard vs dedicated

**Standard** — general-purpose shared compute: data engineering / ETL pipelines, collaborative data science, interactive exploration, cost optimization (multiple users share one resource).

**Dedicated** — when you need RDD APIs, distributed ML frameworks requiring privileged machine access, GPU workloads, or R.

## Language and runtime support

| Language | Support |
|---|---|
| Python | Full — all Databricks Runtime versions |
| SQL | Full — all Databricks Runtime versions |
| Scala | DBR 13.3 LTS+ with Unity Catalog only |
| R | **Not supported** |

## Lakeguard

Standard compute uses **Databricks Lakeguard** for user isolation and data governance — advanced code-isolation techniques that separate each user's code from the underlying Spark infrastructure, enabling safe multi-user sharing. See [[lakeguard]].

Related: [[classic-compute-overview]], [[classic-compute-configure]], [[dedicated-compute-overview]], [[lakeguard]], [[serverless-limitations]].
