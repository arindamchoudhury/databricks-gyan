# Dedicated compute overview

> **Source:** [docs.databricks.com/aws/en/compute/dedicated-overview](https://docs.databricks.com/aws/en/compute/dedicated-overview)
> **Added:** 2026-06-16
> **Source updated:** 2026-06-11
> **Tags:** compute, classic-compute, access-modes, dedicated, single-user, RDD, GPU, R, B1
> **Type:** documentation

> "Dedicated compute is compute configured with dedicated access mode. This means the compute resource can only be used by the single user or group assigned to it."

Dedicated is **single-user or single-group** compute (no multi-user sharing) — needed specifically when a workload requires **RDD APIs, GPUs, R, or privileged machine access**. For everything else, [[standard-compute-overview]] is cheaper and simpler. Group assignment is Public Preview.

## Access mode selection

Configured in the **Advanced** section during compute creation; API field `data_security_mode`. Default is **Auto**: resolves to Standard unless an ML runtime or DBR < 14.3 is selected, in which case Dedicated is used. See [[classic-compute-configure]].

## When to use dedicated compute

Use dedicated *only* when you need one of:

| Reason | Detail |
|---|---|
| **RDD APIs** | Direct access to Spark's Resilient Distributed Dataset API layer |
| **GPU instances** | GPU-accelerated compute for deep learning, distributed ML |
| **R language** | R is not supported on standard compute at all |
| **Privileged machine access** | Lower-level system resource access not available on standard |

All other workloads → use standard compute for cost efficiency and simpler management.

## User and group assignment

- **Single user** — exclusive access for one user only.
- **Single group** *(Public Preview)* — shared access within one group; only one group can be assigned, and it's not equivalent to standard's open multi-user model.

## Fine-grain access control

Requires Databricks Runtime **15.4 LTS+** and **serverless compute enablement** in the workspace.

Related: [[standard-compute-overview]], [[classic-compute-configure]], [[classic-compute-overview]], [[lakeguard]], [[serverless-limitations]].
